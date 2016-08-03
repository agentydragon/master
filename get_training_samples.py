#!/usr/bin/python

"""
Creates positive training samples for distant supervision.

Usage:
    ./get_training_samples.py \
        --article_sentences_entities=allan_dwan.json \
        --article_sentences_entities=autism.json
"""

import argparse
parser = argparse.ArgumentParser(description='Prepare distant supervision positive training samples')
parser.add_argument('--article_sentences_entities', action='append',
                    help='Output from get_sentences_entities.')
args = parser.parse_args()

import json
import myutil

myutil.load_cache()

sentences = []
for jsonfile in args.article_sentences_entities:
    with open(jsonfile) as f:
        sentences.extend(json.loads(f.read()))

all_wikidata_ids = set()
for sentence in sentences:
    all_wikidata_ids = all_wikidata_ids.union(sentence['wikidata_ids'])

# get all relations
print(all_wikidata_ids)

all_pairs = {}
for wikidata_id in all_wikidata_ids:
    for e1, rel, e2 in myutil.wikidata_query(wikidata_id):
        if e1 + "--" + e2 not in all_pairs:
            all_pairs[e1 + "--" + e2] = []
        all_pairs[e1 + "--" + e2].append(rel)
print(all_pairs)

training_data = {}

for sentence in sentences:
    for e1 in sentence['wikidata_ids']:
        for e2 in sentence['wikidata_ids']:
            key = e1 + "--" + e2
            if key in all_pairs:
                # TODO: skip sentence if there are multiple candidate relations
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
with open('training_data.json', 'w') as f:
    f.write(json.dumps(training_data))

myutil.save_cache()
