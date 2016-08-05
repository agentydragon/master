#!/usr/bin/python3

import training_samples_pb2
import myutil
import json

#with open('../training-samples.json') as f:
with open('training-samples.pb', 'rb') as f:
    training_samples = training_samples_pb2.TrainingSamples()
    training_samples.ParseFromString(f.read())

for relation_samples in training_samples.relation_samples:
    relation = relation_samples.relation
    print(relation, myutil.get_name(relation))
    for sample in relation_samples.positive_samples:
        e1, e2 = sample.e1, sample.e2
        text = sample.sentence.text
        sane_text = text[:100].replace('\n', ' ')
        print('\t', myutil.get_name(e1), '\t', myutil.get_name(e2), '\t', sane_text)
