#!/usr/bin/python3

"""
Usage:
    ./metacentrum_spotlight.py \
        --article_plaintexts_dir=/mnt/crypto/data/wiki-articles \
        --outputs_dir=... \
        --max_queries=10 \
        --sleep_between_queries=1
"""

import sys
import time

import paths

import argparse
parser = argparse.ArgumentParser(description='Look up articles in Spotlight')
parser.add_argument('--article_plaintexts_dir',
                    default=paths.WIKI_ARTICLES_PLAINTEXTS_DIR)
parser.add_argument('--outputs_dir',
                    default=paths.SPOTLIGHT_ANNOTATIONS_DIR)
parser.add_argument('--max_queries', type=int,
                    default=-1)
parser.add_argument('--sleep_between_queries', type=int,
                    default=10)
args = parser.parse_args()

# TODO: skip if finished

import json
import os.path
import spotlight

queries = 0

if not os.path.isdir(args.outputs_dir):
    os.makedirs(args.outputs_dir)

filepaths_sanenames = []

for root, subdirs, files in os.walk(args.article_plaintexts_dir):
    for filename in files:
        file_path = os.path.join(root, filename)

        article_sanename = '.'.join(filename.split('.')[:-1])
        filepaths_sanenames.append((file_path, article_sanename))

filepaths_sanenames.sort()

for file_path, article_sanename in filepaths_sanenames:
    output_path = os.path.join(args.outputs_dir, article_sanename + '.spotlight.json')
    if os.path.isfile(output_path):
        print(article_sanename, "-- already annotated")
        continue
    else:
        print(article_sanename)

    text = open(file_path).read()
    try:
        result = spotlight.annotate_text(text)
        queries += 1

        with open(output_path, 'w') as f:
            f.write(json.dumps(result))
    except ValueError as e:
        # TODO: BAD!
        print('cannot process!')
        print(e)

    if args.max_queries >= 0 and queries >= args.max_queries:
        print("max queries exceeded")
        sys.exit(0)

    time.sleep(args.sleep_between_queries)
