"""
Creates positive training samples for distant supervision.

Usage:
    ./get_training_samples.py \
        --article_sentences_entities=allan_dwan.json \
        --article_sentences_entities=autism.json \
        ... \
        --output_file=x.json
"""

from google.protobuf import text_format
import relations
import file_util
import sentence_pb2
import training_samples_pb2
import wikidata

class MentionInSentence(object):
    def __init__(self, start_token_id, end_token_id, wikidata_id):
        self.start_token_id = start_token_id
        self.end_token_id = end_token_id
        self.wikidata_id = wikidata_id

class SentenceInDocument(object):
    def __init__(self, document, sentence_id):
        self.mentions = []
        wikidata_ids = set()
        for coreference in document.coreferences:
            if not coreference.wikidataEntityId:
                # entity not detected
                continue
            for mention in coreference.mentions:
                if mention.sentenceId == sentence_id:
                    self.mentions.append(MentionInSentence(mention.startWordId,
                                                           mention.endWordId,
                                                           coreference.wikidataEntityId))
                    wikidata_ids.add(coreference.wikidataEntityId)
        self.wikidata_ids = list(wikidata_ids)
        self.document = document
        self.sentence_id = sentence_id

        # print(self.get_text(), self.wikidata_ids)

    def all_entity_pairs(self):
        pairs = []
        for e1 in self.wikidata_ids:
            if e1 is None:
                # TODO: HAX SHOULD NOT BE NEEDED
                continue
            for e2 in self.wikidata_ids:
                if e2 is None:
                    # TODO: HAX SHOULD NOT BE NEEDED
                    continue
                pairs.append((e1, e2))
        return pairs

    def get_sentence(self):
        for sentence in self.document.sentences:
            if sentence.id == self.sentence_id:
                return sentence

    def get_text(self):
        return self.get_sentence().text

    def to_sample(self, relation, e1, e2, positive):
        assert (e1 in self.wikidata_ids) and (e2 in self.wikidata_ids)

        sample = training_samples_pb2.TrainingSample()
        sample.positive = positive
        sample.relation = relation
        sample.e1 = e1
        sample.e2 = e2

        sentence = self.get_sentence()

        for mention in self.mentions:
            for token_index in range(mention.start_token_id - 1, mention.end_token_id - 1):
                if mention.wikidata_id == e1:
                    sample.e1_token_indices.append(token_index)
                if mention.wikidata_id == e2:
                    sample.e2_token_indices.append(token_index)

        s = sample.sentence
        s.text = sentence.text
        sentence_start = sentence.tokens[0].start_offset
        for token in sentence.tokens:
            out_token = s.tokens.add()
            out_token.start_offset = token.start_offset - sentence_start
            out_token.end_offset = token.end_offset - sentence_start
            out_token.lemma = token.lemma
            out_token.pos = token.pos
            out_token.ner = token.ner

        return sample

def get_true_triples_expressed_by_sentence(sentence):
    """
    Returns:
        dict (key: "Rxxx", value: ("Q123", "Q456"))
    """
    mentioned_wikidata_ids = sentence.wikidata_ids
    sentence_entity_pairs = sentence.all_entity_pairs()
    wikidata_client = wikidata.WikidataClient()

    all_pairs = {}
    # print(mentioned_wikidata_ids)
    # print(sentence_entity_pairs)
    for wikidata_id in mentioned_wikidata_ids:
        for e1, rel, e2 in wikidata_client.get_all_triples_of_entity(wikidata_id):
            # print('(', e1, rel, e2, ')')
            key = (e1, e2)
            if key not in sentence_entity_pairs:
                # The relation holds, but the entity pair is in no sentences.
                continue
            if key not in all_pairs:
                # TODO: FIXME: relations are returned twice -- forward and backward
                all_pairs[key] = set()
            all_pairs[key].add(rel)
    return all_pairs

def sentence_to_training_data(sentence):
    """
    Args:
      sentence (SentenceInDocument)
    """
    print('sentence_to_training_data(', sentence.get_text(), ')')
    all_pairs = get_true_triples_expressed_by_sentence(sentence)

    print(sentence) #, all_pairs)
    #if len(all_pairs) > 0:
        #raise

    # Add positive samples for represented relations.
    # TODO: skip sentence if there are multiple candidate relations
    training_data = TrainingData()
    for entity_pair, true_relations in all_pairs.items():
        e1, e2 = entity_pair
        for relation in all_pairs[entity_pair]:
            print('\tpositive:', (e1, relation, e2))
            sample = sentence.to_sample(relation, e1, e2, positive=True)
            training_data.add_sample(sample)

    # TODO: add negative samples
    # Add negative samples for unrepresented relations.
    if len(sentence.wikidata_ids) >= 2:
        e1, e2 = sentence.wikidata_ids[:2]
        key = (e1, e2)
        for relation in relations.IMPORTANT_RELATIONS:
            if (key not in all_pairs) or (relation not in all_pairs[key]):
                print('\tnegative:', (e1, relation, e2))
                sample = sentence.to_sample(relation, e1, e2, positive=False)
                training_data.add_sample(sample)

    return training_data

def load_document(document):
    print('Loading document:', document.article_sanename, '...')
    sentences = []
    for sentence in document.sentences:
        # TODO: create more complex samples
        sentences.append(SentenceInDocument(document, sentence.id))
    return sentences

def load_document_files(files):
    """
    Returns:
      list of SentenceInDocument
    """
    sentences = []
    for path in files:
        document = file_util.parse_proto_file(sentence_pb2.Document, path)
        sentences.extend(load_document(document))
    return sentences

def join_sentences_entities(sentences):
    """
    Args:
      sentences (list of SentenceInDocument)
    """
    training_data = TrainingData()
    for sentence in sentences:
        sentence_training_data = sentence_to_training_data(sentence)
        training_data.add_training_data(sentence_training_data)
    return training_data

class TrainingData(object):
    def __init__(self):
        # key: relation id, value: list of samples, both positive and negative
        self.training_data = {}

    def load(self, path):
        td = file_util.parse_proto_file(
            training_samples_pb2.TrainingSamples,
            path)
        # TODO
        self.training_data = {}
        for relation_training_samples in td.relation_samples:
            self.training_data[relation_training_samples.relation] = (
                [sample for sample in relation_training_samples.samples])

    def add_sample(self, sample):
        if sample.relation not in self.training_data:
            self.training_data[sample.relation] = []
        # TODO: training data should also say where is the
        # relevant mention
        self.training_data[sample.relation].append(sample)

    def add_training_data(self, other):
        for relation, samples in other.training_data.items():
            if relation not in self.training_data:
                self.training_data[relation] = []
            self.training_data[relation].extend(samples)

    def to_proto(self):
        samples = training_samples_pb2.TrainingSamples()
        for relation, rs in self.training_data.items():
            rels = samples.relation_samples.add()
            rels.relation = relation
            rels.samples.extend(rs)
        return samples

    def write(self, output_file):
        samples = self.to_proto()
        # print(text_format.MessageToString(samples))
        with open(output_file, 'wb') as f:
            f.write(samples.SerializeToString())
