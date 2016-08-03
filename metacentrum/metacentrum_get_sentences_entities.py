#!/usr/bin/python3

"""
TODO

Usage:
    TODO
"""

import argparse
import os.path

parser = argparse.ArgumentParser(description='TODO')
parser.add_argument('--plaintexts_dir')
parser.add_argument('--parse_xmls_dir')
parser.add_argument('--spotlight_jsons_dir')
parser.add_argument('--outputs_dir')
args = parser.parse_args()

if not os.path.isdir(args.outputs_dir):
    os.makedirs(args.outputs_dir)

import myutil
import article_parse

import json

for root, subdirs, files in os.walk(args.plaintexts_dir):
    for filename in files:
        plaintext_path = os.path.join(root, filename)
        article_sanename = '.'.join(filename.split('.')[:-1])

        # (parse_xmls_dir)/Anarchism_in_France.txt.out
        # (spotlight_jsons)/Anarchism_in_France.spotlight.json
        parse_path = os.path.join(args.parse_xmls_dir, article_sanename + ".txt.out")
        if not os.path.isfile(parse_path):
            # print(article_sanename, "skipped, not parsed")
            continue

        spotlight_path = os.path.join(args.spotlight_jsons_dir, article_sanename + ".spotlight.json")
        if not os.path.isfile(spotlight_path):
            # print(article_sanename, "skipped, parsed but not spotlighted")
            continue

        print(article_sanename, "processing")
        parse = article_parse.ArticleParse()
        parse.load(plaintext_path, spotlight_path, parse_path)
        parse.annotate_sentences_with_wikidata_ids()

        json_data = parse.get_sentences_with_wikidata_ids()

        output_path = os.path.join(args.outputs_dir, article_sanename + ".sentences_entities.json")
        with open(output_path, 'w') as f:
            f.write(json.dumps(json_data))

        myutil.save_cache()
