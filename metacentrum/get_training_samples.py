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

def join_sentences_entities(article_sentences_entities, output_file):
    sentences = []
    for jsonfile in article_sentences_entities:
        with open(jsonfile) as f:
            sentences.extend(json.loads(f.read()))

    all_wikidata_ids = set()
    for sentence in sentences:
        all_wikidata_ids = all_wikidata_ids.union(sentence['wikidata_ids'])

    all_pairs_in_sentences = set()
    for sentence in sentences:
        sentence_entity_pairs = all_sentence_entity_pairs(sentence)
        all_pairs_in_sentences = all_pairs_in_sentences.union(sentence_entity_pairs)

    # key: (e1---e2). value: list of relations between entities
    all_pairs = {}
    for wikidata_id in all_wikidata_ids:
        for e1, rel, e2 in myutil.wikidata_query(wikidata_id):
            key = (e1, e2)
            if key not in all_pairs_in_sentences:
                # The relation holds, but the entity pair is in no sentences.
                continue
            if key not in all_pairs:
                # TODO: FIXME: relations are returned twice -- forward and backward
                all_pairs[key] = set()
            all_pairs[key].add(rel)
    print(all_pairs)

    training_data = {}

    for sentence in sentences:
        sentence_entity_pairs = set(all_sentence_entity_pairs(sentence))
        represented_entity_pairs_in_relations = sentence_entity_pairs.intersection(all_pairs.keys())

        # TODO: skip sentence if there are multiple candidate relations
        for e1, e2 in represented_entity_pairs_in_relations:
            key = (e1, e2)
            for relation in all_pairs[key]:
                if relation not in training_data:
                    training_data[relation] = []
                training_data[relation].append({
                    # TODO: training data should also say where is the
                    # relevant mention
                    'sentence': sentence,
                    'e1': e1,
                    'e2': e2
                })
    with open(output_file, 'w') as f:
        f.write(json.dumps(training_data))

def main():
    parser = argparse.ArgumentParser(description='Prepare distant supervision positive training samples')
    parser.add_argument('--article_sentences_entities', action='append',
                        help='Output from get_sentences_entities.')
    parser.add_argument('--output_file')
    args = parser.parse_args()

    myutil.load_cache()
    join_sentences_entities(args.article_sentences_entities, args.output_file)
    myutil.save_cache()
