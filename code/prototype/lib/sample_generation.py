import paths
from xml.etree import ElementTree
from prototype.lib import article_repo
from prototype.lib import training_sample
from prototype.lib import relations
import random

def try_load_document(article_title):
    article_repository = article_repo.ArticleRepo()

    # print(article_title)
    if not article_repository.article_exists(article_title):
        print('article', article_title, 'does not exist')
        return

    article = article_repository.load_article(article_title)
    if not article.corenlp_xml:
        print('unparsed article', article_title)
        return

    if not article.spotlight_json:
        print('unspotlighted article', article_title)
        return

    if not article.sentences:
        print('unjoined article', article_title)
        return

    return article

def get_document_subgraph(document, wikidata_client, relations):
    all_wikidata_ids = set()
    all_triples = set()
    WIKIDATA_IDS_PER_BATCH = 20

    for sentence in document.sentences:
        sentence_wrapper = SentenceWrapper(document, sentence)
        all_wikidata_ids = all_wikidata_ids.union(sentence_wrapper.get_sentence_wikidata_ids())

        if len(all_wikidata_ids) >= WIKIDATA_IDS_PER_BATCH:
            all_triples = all_triples.union(wikidata_client.get_triples_between_entities(
                all_wikidata_ids,
                relations = relations
            ))
            all_wikidata_ids = set()

    all_triples = all_triples.union(wikidata_client.get_triples_between_entities(
        all_wikidata_ids,
        relations = relations
    ))
    return all_triples

def get_all_document_entities(document):
    all_wikidata_ids = set()
    for sentence in document.sentences:
        sentence_wrapper = SentenceWrapper(document, sentence)
        all_wikidata_ids = all_wikidata_ids.union(sentence_wrapper.get_sentence_wikidata_ids())
    return all_wikidata_ids

def get_all_document_samples(document):
    samples = []

    all_wikidata_ids = get_all_document_entities(document)

    for sentence in document.sentences:
        sentence_wrapper = SentenceWrapper(document, sentence)
        wikidata_ids = sentence_wrapper.get_sentence_wikidata_ids()

        for subject in wikidata_ids:
            for object in wikidata_ids:
                # Against reflexive references ("Country is in country").
                if sentence_wrapper.mentions_in_sentence_overlap(subject, object):
                    continue

                sample = sentence_wrapper.make_training_sample(
                    s = subject,
                    relation = None,
                    o = object,
                    positive = None
                )
                samples.append(sample)

    # print('Document produced', len(samples), 'unlabeled samples.')
    return samples

def get_document_samples(document, wikidata_client):
    samples = []

    all_triples = get_document_subgraph(
        document,
        wikidata_client,
        relations = relations.RELATIONS
    )

    all_wikidata_ids = get_all_document_entities(document)
    document_subject_relation_pairs = wikidata_client.get_subject_relation_pairs(
        all_wikidata_ids,
        relations = relations.RELATIONS
    )
    document_object_relation_pairs = wikidata_client.get_object_relation_pairs(
        all_wikidata_ids,
        relations = relations.RELATIONS
    )

    for sentence in document.sentences:
        sentence_wrapper = SentenceWrapper(document, sentence)
        wikidata_ids = sentence_wrapper.get_sentence_wikidata_ids()

        sentence_subject_relation_pairs = [(subject, relation)
                                           for subject, relation in document_subject_relation_pairs
                                           if subject in wikidata_ids]
        sentence_object_relation_pairs = [(object, relation)
                                           for object, relation in document_object_relation_pairs
                                           if object in wikidata_ids]

#        sentence_relations = wikidata_client.get_all_relations_of_entities(wikidata_ids)
#
        # subject_relation_pairs = wikidata_client.get_subject_relation_pairs(wikidata_ids)
        # object_relation_pairs = wikidata_client.get_object_relation_pairs(wikidata_ids)
        sentence_relations = []
        sentence_relations += list(set(relation for subject, relation in
                                       sentence_subject_relation_pairs))
        sentence_relations += list(set(relation for object, relation in
                                       sentence_object_relation_pairs))
        sentence_relations = set(sentence_relations)

        for relation in sentence_relations:
            # subject_wikidata_ids = wikidata_client.find_relation_subjects(wikidata_ids, relation)
            # object_wikidata_ids = wikidata_client.find_relation_objects(wikidata_ids, relation)
            subject_wikidata_ids = list(set(subject for subject, r in sentence_subject_relation_pairs if r == relation))
            object_wikidata_ids = list(set(object for object, r in sentence_object_relation_pairs if r == relation))

            for subject in wikidata_ids:
                for object in wikidata_ids:
                    # Against reflexive references ("Country is in country").
                    if sentence_wrapper.mentions_in_sentence_overlap(subject, object):
                        continue

                    if (subject, relation, object) in all_triples:
                        # True relation. Not a negative.
                        sample = sentence_wrapper.make_training_sample(
                            subject,
                            relation,
                            object,
                            positive = True
                        )
                        samples.append(sample)
                        continue

                    subject_has_counterexample = (subject in subject_wikidata_ids)
                    object_has_counterexample = (object in object_wikidata_ids)
                    has_counterexample = (subject_has_counterexample or
                                          object_has_counterexample)
                    if has_counterexample:
                        # This sentence is false (LCWA)
                        sample = sentence_wrapper.make_training_sample(
                            subject,
                            relation,
                            object,
                            positive = False
                        )
                        samples.append(sample)
                        continue

                    # Sentence may be either true or false.
                    continue

    print('Document produced', len(samples), 'true+false samples.')
    return samples

def get_samples_from_document(article_title, wikidata_client):
    document = try_load_document(article_title)
    if not document:
        print('cannot load document')
        return
    return get_document_samples(document, wikidata_client)

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
            if mention.wikidata_id == entity:
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
            wikidata_id = mention.wikidata_id
            if not wikidata_id:
                continue

            # Also check that some tokens actually have this ID.
            if len(self.find_sentence_token_idxs_of_entity(wikidata_id)) == 0:
                # TODO: hack
                continue

            wikidata_ids.add(wikidata_id)

        return wikidata_ids
