#!/usr/bin/python3

# TODO

import os
import file_util
from google.protobuf import text_format
import get_training_samples
import sentence_pb2
import training_samples_pb2
import json
import wikidata

import argparse

###def is_person(wikidata_id):
###    TODO
###
###def are_married(e1, e2):
###    TODO
###
###def has_spouse(e1):
###    TODO

def main():
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('--annotated_documents_dir', required=True)
    parser.add_argument('--input_training_data', required=True)
    parser.add_argument('--max_sentences', type=int, required=True)
    parser.add_argument('--output_training_data', required=True)
    args = parser.parse_args()

    paths = []
    for root, subdirs, files in os.walk(args.annotated_documents_dir):
        for filename in files:
            path = os.path.join(root, filename)
            paths.append(path)
    print("paths:", paths)

    sentences = get_training_samples.load_document_files(paths)
    if args.max_sentences > 0:
        sentences = sentences[:args.max_sentences]

    ## collect negative samples for P26 "is married"
    #for sentence in sentences:
    #    # if sentence contains two people
    #    # and the two people are not married
    #    # ==> use the sentence as negative sample
    #    for e1, e2 in sentence.all_entity_pairs:
    #        if is_person(e1) and is_person(e2):
    #            if not is_married(e1, e2) and has_spouse(e1) and has_spouse(e2):
    #                print(e1, e2, sentence)

    training_data = file_util.parse_proto_file(
        training_samples_pb2.TrainingSamples,
        args.input_training_data)
    for relation_training_samples in training_data.relation_samples:
        relation = relation_training_samples.relation
        #if relation != 'P26':
        #    continue

        print(relation)

        for sentence in sentences:
            triples = get_training_samples.get_true_triples_expressed_by_sentence(sentence)

            if len(sentence.wikidata_ids) < 2:
                continue

            e1, e2 = sentence.wikidata_ids[:2]

            if relation not in triples:
                print('negative for %s:' % relation, sentence.get_text())
                sample = sentence.to_sample(relation, e1, e2, positive=False)
                relation_training_samples.negative_samples.extend([sample])

        # TODO: generate negative samples from bad mentions, too?
        # TODO: add negative constraints, too?

    with open(args.output_training_data, 'wb') as f:
        f.write(training_data.SerializeToString())

    #training_data.write(args.output_file)

if __name__ == '__main__':
    main()
