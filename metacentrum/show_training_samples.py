#!/usr/bin/python3

import myutil
import json

#with open('../training-samples.json') as f:
with open('training-samples.json') as f:
    training_samples = json.loads(f.read())

for relation, samples in sorted(training_samples.items()):
    print(relation, myutil.get_name(relation))
    for sample in samples:
        e1, e2 = sample['e1'], sample['e2']
        text = sample['sentence']['text']
        sane_text = text[:100].replace('\n', ' ')
        print('\t', myutil.get_name(e1), '\t', myutil.get_name(e2), '\t', sane_text)
