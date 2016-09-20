from prototype.lib import parse_xmls_to_protos
from prototype.lib import article_repo
from prototype.lib import sample_repo
from prototype.lib import training_sample
from py import paths
from py import wikidata
from py import dbpedia
from xml.etree import ElementTree
import json
import argparse
import multiprocessing

wikidata_client = None

def find_sentence_token_idxs_of_entity(document, sentence, entity):
    mentions = []
    for mention in document.find_spotlight_mentions_between(sentence.start_offset(),
                                                            sentence.end_offset()):
        wikidata_id = dbpedia.dbpedia_uri_to_wikidata_id(mention.uri)
        if wikidata_id == entity:
            mentions.append(mention)

    # now we have all mentions of the entity in the sentence
    tokens_idxs = set()
    for i, token in enumerate(sentence.tokens):
        for mention in mentions:
            if token.start_offset >= mention.start_offset and token.end_offset <= mention.end_offset:
                tokens_idxs.add(i)
    return list(sorted(tokens_idxs))

def make_training_sample(document, sentence, s, relation, o):
    sample = training_sample.TrainingSample(
        relation = relation,
        positive = True,
        sentence = training_sample.TrainingSampleParsedSentence(
            text = sentence.text,
            tokens = []
        ),
        subject = s,
        object = o,
        subject_token_indices = find_sentence_token_idxs_of_entity(document, sentence, s),
        object_token_indices = find_sentence_token_idxs_of_entity(document, sentence, o)
    )

    for token in sentence.tokens:
        sample.sentence.tokens.append(
            training_sample.TrainingSampleSentenceToken(
                start_offset = token.start_offset - sentence.start_offset(),
                end_offset = token.end_offset - sentence.start_offset(),
                lemma = token.lemma,
                pos = token.pos,
                ner = token.ner
            )
        )

    # TODO: Mark all tokens that overlap the mention

    return sample

def process_article(article_title):
    print(article_title)
    if not article_repo.article_exists(paths.WIKI_ARTICLES_PLAINTEXTS_DIR,
                                       article_title):
        print('article does not exist')
        return

    article = article_repo.load_article(paths.WIKI_ARTICLES_PLAINTEXTS_DIR,
                                        article_title)
    if 'corenlp_xml' not in article or 'spotlight_json' not in article:
        print('incomplete')
        return

    document = parse_xmls_to_protos.document_to_proto(
        root = ElementTree.fromstring(article['corenlp_xml']),
        plaintext = article['plaintext'],
        spotlight_json = article['spotlight_json']
    )

    samples = {}

    for sentence in document.sentences:
        wikidata_ids = set()
        for mention in document.find_spotlight_mentions_between(sentence.start_offset(),
                                                                sentence.end_offset()):
            wikidata_id = dbpedia.dbpedia_uri_to_wikidata_id(mention.uri)
            if wikidata_id:
                wikidata_ids.add(wikidata_id)

        for s, p, o in wikidata_client.get_triples_between_entities(wikidata_ids):
            if p not in samples:
                samples[p] = []

            print(p, s, o, sentence.text)
            samples[p].append(make_training_sample(document, sentence, s, p, o))

    try:
        sample_repo.write_article(article_title, samples)
    except sample_repo.SavingError as e:
        print("Error during processing article '%s'" % article_title)
        print(e)
    except:
        print("Error during processing article '%s'" % article_title)
        print(e)
        raise
    return

def main():
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('--articles', action='append')
    parser.add_argument('--wikidata_endpoint')
                        # description='example: https://query.wikidata.org/sparql, or http://hador:3030/wikidata/query')
    parser.add_argument('--parallelism', default=1, type=int)
    args = parser.parse_args()

    global wikidata_client
    wikidata_client = wikidata.WikidataClient(args.wikidata_endpoint or None)

    assert args.parallelism >= 1
    if args.parallelism == 1:
        for article in args.articles:
            process_article(article)
    else:
        pool = multiprocessing.Pool(args.parallelism)
        pool.map(process_article, args.articles)

if __name__ == '__main__':
    main()
