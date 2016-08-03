#!/usr/bin/python3

"""
TODO

Usage:
    TODO
"""

import os.path
import get_training_samples
import argparse
import myutil

def main():
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('--sentences_entities_dir')
    parser.add_argument('--output_file')
    args = parser.parse_args()

    paths = []
    for root, subdirs, files in os.walk(args.sentences_entities_dir):
        for filename in files:
            path = os.path.join(root, filename)
            paths.append(path)
    print(paths)

    myutil.load_cache()
    get_training_samples.join_sentences_entities(paths, args.output_file)
    myutil.save_cache()

main()
