from prototype.lib import parse_xmls_to_protos
from prototype.lib import article_repo
from prototype.lib import sample_repo
from py import paths
from py import wikidata
from py import dbpedia
from xml.etree import ElementTree
import json

def process_article(article_title):
    print(article_title)
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

    client = wikidata.WikidataClient()

    for sentence in document.sentences:
        wikidata_ids = set()
        for mention in document.find_spotlight_mentions_between(sentence.start_offset(),
                                                                sentence.end_offset()):
            wikidata_id = dbpedia.dbpedia_uri_to_wikidata_id(mention.uri)
            if wikidata_id:
                wikidata_ids.add(wikidata_id)

            for s, p, o in client.get_triples_between_entities(wikidata_ids):
                if p not in samples:
                    samples[p] = []

                print(p, s, o, sentence.text)
                samples[p].append((s, o, sentence.text))

    sample_repo.write_article(article_title, samples)

def main():
    import argparse
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('--articles', action='append')
    args = parser.parse_args()

    for article in args.articles:
        process_article(article)

if __name__ == '__main__':
    main()
