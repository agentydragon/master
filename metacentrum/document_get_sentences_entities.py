#!/usr/bin/python3

"""
Creates list of Wikidata entities mentioned in each sentence
by joining Spotlight's entity linking with CoreNLP's coreference resolution.

Usage:
    ./document_sentences_entities.py \
        --article_plaintext_path=/mnt/crypto/data/wiki-articles/Allan_Dwan.txt \
        --article_parse_xml_path=Allan_Dwan.txt.out \
        --article_spotlight_json_path=Allan_Dwan.spotlight.json \
        --output_path=allan_dwan.json
"""

import argparse

parser = argparse.ArgumentParser(description='Propagace entity links through coreferences')
parser.add_argument('--article_plaintext_path', type=str)
parser.add_argument('--article_parse_xml_path', type=str)
parser.add_argument('--article_spotlight_json_path', type=str)
parser.add_argument('--output_path', type=str)
args = parser.parse_args()

import article_parse

import json

parse = article_parse.ArticleParse()
parse.load(args.article_plaintext_path, args.article_spotlight_json_path, args.article_parse_xml_path)
parse.annotate_sentences_with_wikidata_ids()

json_data = []
json_data.extend(parse.get_sentences_with_wikidata_ids())
with open(args.output_path, 'w') as f:
    f.write(json.dumps(json_data))
