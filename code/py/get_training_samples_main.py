#!/usr/bin/python3

"""
TODO

Usage:
    TODO
"""

import os.path
import sentence_pb2
import file_util
import get_training_samples
import argparse

def main():
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('--annotated_documents_dir', required=True)
    parser.add_argument('--intermediate_dir', required=True)
    parser.add_argument('--output_file', required=True)
    parser.add_argument('--max_documents', type=int, required=True)
    args = parser.parse_args()

    file_util.ensure_dir(args.intermediate_dir)

    paths = list(file_util.recursive_subfile_paths(args.annotated_documents_dir))
    print("paths:", paths)

    documents = 0
    training_data = get_training_samples.TrainingData()
    for path in paths:
        document = file_util.parse_proto_file(sentence_pb2.Document, path)
        # TODO: retarded extension
        document_training_data_path = (args.intermediate_dir + '/' +
                                       document.article_sanename + ".txt")

        if os.path.isfile(document_training_data_path):
            print("Loading from cache:", document.article_sanename)
            document_training_data = get_training_samples.TrainingData()
            document_training_data.load(document_training_data_path)
        else:
            print("Remarking:", document.article_sanename)
            sentences = get_training_samples.load_document(document)
            document_training_data = get_training_samples.join_sentences_entities(sentences)
            document_training_data.write(document_training_data_path)

        training_data.add_training_data(document_training_data)

        documents += 1
        if documents > args.max_documents:
            break

    training_data.write(args.output_file)

    #sentences = get_training_samples.load_document_files(paths)
    #if args.max_sentences > 0:
    #    sentences = sentences[:args.max_sentences]

if __name__ == '__main__':
    main()
