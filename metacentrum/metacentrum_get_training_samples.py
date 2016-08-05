#!/usr/bin/python3

"""
TODO

Usage:
    TODO
"""

import os.path
import get_training_samples
import argparse

def main():
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('--annotated_documents_dir', required=True)
    parser.add_argument('--output_file', required=True)
    parser.add_argument('--max_sentences', type=int, required=True)
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
    training_data = get_training_samples.join_sentences_entities(sentences)
    training_data.write(args.output_file)

main()
