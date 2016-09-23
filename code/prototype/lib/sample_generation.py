import paths
from xml.etree import ElementTree
from prototype.lib import dbpedia
from prototype.lib import parse_xmls_to_protos
from prototype.lib import article_repo
from prototype.lib import training_sample
import random

def try_load_document(article_title):
    # print(article_title)
    if not article_repo.article_exists(article_title):
        print('article', article_title, 'does not exist')
        return

    article = article_repo.load_article(paths.WIKI_ARTICLES_PLAINTEXTS_DIR,
                                        article_title)
    if 'corenlp_xml' not in article or 'spotlight_json' not in article:
        print('incomplete article', article_title)
        return

    return parse_xmls_to_protos.document_to_proto(
        root = ElementTree.fromstring(article['corenlp_xml']),
        plaintext = article['plaintext'],
        spotlight_json = article['spotlight_json']
    )

def get_samples_from_document(article_title, wikidata_client):
    document = try_load_document(article_title)
    if not document:
        print('cannot load document')
        return

    samples = {}

    for sentence in document.sentences:
        sentence_wrapper = SentenceWrapper(document, sentence)
        wikidata_ids = sentence_wrapper.get_sentence_wikidata_ids()

        for s, p, o in wikidata_client.get_triples_between_entities(wikidata_ids):
            if p not in samples:
                samples[p] = []

            # Against reflexive references ("Country is in country").
            if sentence_wrapper.mentions_in_sentence_overlap(s, o):
                continue

            print(p, s, o, sentence.text)
            sample = sentence_wrapper.make_training_sample(s, relation, o,
                                                           positive=True)
            samples[p].append(sample)
    return samples

def sample_random_entity_pair(documents):
    while True:
        document = random.choice(documents)

        for i in range(5):
            # select random sentence that has at least 2 mentions in it
            sentence = random.choice(document.sentences)
            sentence_wrapper = SentenceWrapper(document, sentence)

            wikidata_ids = sentence_wrapper.get_sentence_wikidata_ids()
            if len(wikidata_ids) < 2:
                continue

            for j in range(5):
                # select two random wikidata ids
                s, o = random.sample(wikidata_ids, 2)

                # Against reflexive references ("Country is in country").
                if sentence_wrapper.mentions_in_sentence_overlap(s, o):
                    continue

                return sentence_wrapper.make_training_sample(s, None, o,
                                                             positive=None)
            # select sentence again
            continue
        # pick next article
        continue

def sample_complete_negative(documents, wikidata_client):
    while True:
        sample = sample_random_entity_pair(documents)
        if len(wikidata_client.get_holding_relations_between(sample.subject,
                                                             sample.object)) > 0:
            # skip if we happen to hit it
            continue
        else:
            sample.relation = None
            sample.positive = False
            return sample

def sample_negative(documents, relation, wikidata_client):
    while True:
        sample = sample_random_entity_pair(documents)
        if wikidata_client.relation_exists(sample.subject, relation, sample.object):
            # skip if we happen to hit it
            continue
        else:
            sample.relation = relation
            sample.positive = False
            return sample

class SentenceWrapper(object):
    def __init__(self, document, sentence):
        self.document = document
        self.sentence = sentence

    def find_sentence_token_idxs_of_entity(self, entity):
        mentions = []
        for mention in self.document.get_spotlight_mentions_in_sentence(self.sentence):
            wikidata_id = dbpedia.dbpedia_uri_to_wikidata_id(mention.uri)
            if wikidata_id == entity:
                mentions.append(mention)

        # now we have all mentions of the entity in the sentence
        tokens_idxs = set()
        for i, token in enumerate(self.sentence.tokens):
            for mention in mentions:
                if (token.start_offset >= mention.start_offset and
                        token.end_offset <= mention.end_offset):
                    tokens_idxs.add(i)
        return list(sorted(tokens_idxs))

    def mentions_in_sentence_overlap(self, s, o):
        si = self.find_sentence_token_idxs_of_entity(s)
        oi = self.find_sentence_token_idxs_of_entity(o)
        return len(set(si) & set(oi)) > 0

    def make_training_sample(self, s, relation, o, positive):
        sample = training_sample.TrainingSample(
            relation = relation,
            positive = positive,
            sentence = training_sample.TrainingSampleParsedSentence(
                text = self.sentence.text,
                tokens = [],
                origin_article = self.document.title,
                origin_sentence_id = self.sentence.id
            ),
            subject = s,
            object = o,
            subject_token_indices = self.find_sentence_token_idxs_of_entity(s),
            object_token_indices = self.find_sentence_token_idxs_of_entity(o)
        )

        assert len(sample.subject_token_indices) > 0
        assert len(sample.object_token_indices) > 0

        for token in self.sentence.tokens:
            sample.sentence.tokens.append(
                training_sample.TrainingSampleSentenceToken(
                    start_offset = token.start_offset - self.sentence.start_offset(),
                    end_offset = token.end_offset - self.sentence.start_offset(),
                    lemma = token.lemma,
                    pos = token.pos,
                    ner = token.ner
                )
            )

        # TODO: Mark all tokens that overlap the mention

        return sample

    def get_sentence_wikidata_ids(self):
        wikidata_ids = set()
        for mention in self.document.get_spotlight_mentions_in_sentence(self.sentence):
            wikidata_id = dbpedia.dbpedia_uri_to_wikidata_id(mention.uri)
            if not wikidata_id:
                continue

            # Also check that some tokens actually have this ID.
            if len(self.find_sentence_token_idxs_of_entity(wikidata_id)) == 0:
                # TODO: hack
                continue

            wikidata_ids.add(wikidata_id)

        return wikidata_ids
