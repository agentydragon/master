#!/usr/bin/python3

"""
Usage:
    ./metacentrum_spotlight.py \
        --article_plaintexts_dir=/mnt/crypto/data/wiki-articles \
        --outputs_dir=... \
        --max_queries=10
"""

import sys

import argparse
parser = argparse.ArgumentParser(description='Look up articles in Spotlight')
parser.add_argument('--article_plaintexts_dir')
parser.add_argument('--outputs_dir')
parser.add_argument('--max_queries', type=int)
args = parser.parse_args()

# TODO: skip if finished

import json
import requests
import os.path

queries = 0
server = 'http://spotlight.sztaki.hu:2222'
url = server + '/rest/annotate'

if not os.path.isdir(args.outputs_dir):
    os.makedirs(args.outputs_dir)

for root, subdirs, files in os.walk(args.article_plaintexts_dir):
    for filename in files:
        file_path = os.path.join(root, filename)

        article_sanename = '.'.join(filename.split('.')[:-1])
        print(article_sanename)

        text = open(file_path).read()
        r = requests.post(url, data={
          'text': text,
          'confidence': '0.35'
        }, headers={'Accept': 'application/json'})
        queries += 1

        output_path = os.path.join(args.outputs_dir, article_sanename + '.spotlight.json')
        with open(output_path, 'w') as f:
            f.write(json.dumps(r.json()))

        if args.max_queries >= 0 and queries >= args.max_queries:
            print("max queries exceeded")
            sys.exit(0)
