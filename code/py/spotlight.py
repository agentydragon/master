#!/usr/bin/python3

"""
Usage:
    ./spotlight.py \
        --article_plaintext_path=/mnt/crypto/data/wiki-articles/Allan_Dwan.txt \
        --output_path=Allan_Dwan.spotlight.json
"""

import argparse

import json
import requests

SPOTLIGHT_SERVER = 'http://spotlight.sztaki.hu:2222/rest/annotate'
# SPOTLIGHT_SERVER = 'http://localhost:2222/rest/annotate'
# SPOTLIGHT_SERVER = 'http://zebra6a:2222/rest/annotate'

def annotate_text(text, spotlight_server=None):
    if spotlight_endpoint is None:
        spotlight_endpoint = SPOTLIGHT_SERVER

    r = requests.post(spotlight_endpoint, data={
      'text': text,
      'confidence': '0.35'
    }, headers={'Accept': 'application/json'})
    try:
        return r.json()
    except:
        print(r.text)
        raise

def main():
    parser = argparse.ArgumentParser(description='Get DBpedia entity mentions using Spotlight')
    parser.add_argument('--article_plaintext_path', required=True)
    parser.add_argument('--output_path', required=True)
    args = parser.parse_args()

    text = open(args.article_plaintext_path).read()
    result = annotate_text(text)
    with open(args.output_path, 'w') as f:
        f.write(json.dumps(result))

if __name__ == '__main__':
    main()
