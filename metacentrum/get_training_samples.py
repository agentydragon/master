#!/usr/bin/python3

"""
Creates positive training samples for distant supervision.

Usage:
    ./get_training_samples.py \
        --article_sentences_entities=allan_dwan.json \
        --article_sentences_entities=autism.json \
        ... \
        --output_file=x.json
"""

import sentence_pb2
#import training_samples_pb2
import argparse
import json
import myutil

def all_sentence_entity_pairs(sentence):
    for e1 in sentence['wikidata_ids']:
        if e1 is None:
            # TODO: HAX SHOULD NOT BE NEEDED
            continue
        for e2 in sentence['wikidata_ids']:
            if e2 is None:
                # TODO: HAX SHOULD NOT BE NEEDED
                continue
            yield (e1, e2)

def sentence_to_training_data(sentence):
    mentioned_wikidata_ids = sentence['wikidata_ids']
    sentence_entity_pairs = set(all_sentence_entity_pairs(sentence))

    all_pairs = {}
    for wikidata_id in mentioned_wikidata_ids:
        for e1, rel, e2 in myutil.wikidata_query(wikidata_id):
            key = (e1, e2)
            if key not in sentence_entity_pairs:
                # The relation holds, but the entity pair is in no sentences.
                continue
            if key not in all_pairs:
                # TODO: FIXME: relations are returned twice -- forward and backward
                all_pairs[key] = set()
            all_pairs[key].add(rel)

    print(sentence, all_pairs)

    # TODO: skip sentence if there are multiple candidate relations
    training_data = TrainingData()
    for entity_pair, true_relations in all_pairs.items():
        e1, e2 = entity_pair
        for relation in all_pairs[entity_pair]:
            # TODO: training data should also say where is the
            # relevant mention
            training_data.add_sample(relation, sentence, e1, e2)

    return training_data

def load_document_files(files):
    sentences = []
    for path in files:
        document = sentence_pb2.Document()
        with open(path, 'rb') as f:
            document.ParseFromString(f.read())

        for sentence in document.sentences:
            # TODO: create more complex samples
            sent = {
                'wikidata_ids': set(),
                'text': sentence.text
            }
            for coreference in document.coreferences:
                if not coreference.wikidataEntityId:
                    # entity not detected
                    continue
                for mention in coreference.mentions:
                    if mention.sentenceIndex == sentence.id:
                        sent['wikidata_ids'].add(coreference.wikidataEntityId)
            sent['wikidata_ids'] = list(sent['wikidata_ids'])
            sentences.append(sent)
    return sentences

def join_sentences_entities(sentences):
    training_data = TrainingData()
    for sentence in sentences:
        sentence_training_data = sentence_to_training_data(sentence)

        training_data.add_training_data(sentence_training_data)
    return training_data

class TrainingData(object):
    def __init__(self):
        # key: relation id, value: list of sentences
        self.training_data = {}

    def add_sample(self, relation, sentence, e1, e2):
        if relation not in self.training_data:
            self.training_data[relation] = []
        self.training_data[relation].append({
            # TODO: training data should also say where is the
            # relevant mention
            'sentence': sentence,
            'e1': e1,
            'e2': e2
        })

    def add_training_data(self, other):
        for relation, samples in other.training_data.items():
            if relation not in self.training_data:
                self.training_data[relation] = []
            self.training_data[relation].extend(samples)

    def write(self, output_file):
        with open(output_file, 'w') as f:
            f.write(json.dumps(self.training_data))

#def main():
#    parser = argparse.ArgumentParser(description='Prepare distant supervision positive training samples')
#    parser.add_argument('--article_sentences_entities', action='append',
#                        help='Output from get_sentences_entities.')
#    parser.add_argument('--output_file')
#    args = parser.parse_args()
#
#    myutil.load_cache()
#    sentences = load_sentence_files(args.article_sentences_entities)
#    training_data = join_sentences_entities(sentences)
#    training_data.write(output_file)
#    myutil.save_cache()
