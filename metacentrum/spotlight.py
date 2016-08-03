#!/usr/bin/python3

"""
Usage:
    ./spotlight.py \
        --article_plaintext_path=/mnt/crypto/data/wiki-articles/Allan_Dwan.txt \
        --output_path=Allan_Dwan.spotlight.json
"""

import argparse
parser = argparse.ArgumentParser(description='Get DBpedia entity mentions using Spotlight')
parser.add_argument('--article_plaintext_path')
parser.add_argument('--output_path')
args = parser.parse_args()

import json
import requests

text = open(args.article_plaintext_path).read()

# server = 'http://localhost:2222'
server = 'http://spotlight.sztaki.hu:2222'
url = server + '/rest/annotate'
r = requests.get(url, params={
  'text': text,
  'confidence': '0.35'
}, headers={'Accept': 'application/json'})
with open(args.output_path, 'w') as f:
    f.write(json.dumps(r.json()))
