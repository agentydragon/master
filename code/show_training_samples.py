#!/usr/bin/python3

import training_samples_pb2
import wikidata
import dbpedia
import json
import argparse

def main():
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('--input_file', required=True)
    args = parser.parse_args()

    wikidata_client = wikidata.WikidataClient()
    wikidata_client.persist_caches = False

    with open(args.input_file, 'rb') as f:
        training_samples = training_samples_pb2.TrainingSamples()
        training_samples.ParseFromString(f.read())

    for relation_samples in training_samples.relation_samples:
        relation = relation_samples.relation
        print(relation, wikidata_client.get_name(relation))
        for sample in relation_samples.samples:
            e1, e2 = sample.e1, sample.e2
            text = sample.sentence.text
            sane_text = text[:100].replace('\n', ' ')
            print('\t', sample.positive, '\t', wikidata_client.get_name(e1), '\t', wikidata_client.get_name(e2), '\t', sane_text)

if __name__ == '__main__':
    main()
