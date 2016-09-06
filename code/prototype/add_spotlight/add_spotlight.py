#!/usr/bin/python3

"""
Usage:
    bazel run :add_spotlight \
        --article=(...) \
        --article=(...)
"""

import sys
import time

from py import paths

import argparse
parser = argparse.ArgumentParser(description='Look up articles in Spotlight')
parser.add_argument('--article_plaintexts_dir',
                    default=paths.WIKI_ARTICLES_PLAINTEXTS_DIR)
parser.add_argument('--articles', action='append')
args = parser.parse_args()

# TODO: skip if finished

import json
import os.path
from py import spotlight
from prototype import article_repo

#queries = 0

for title in args.articles:
    article_data = article_repo.load_article(args.article_plaintexts_dir, title)
    spotlight_json = spotlight.annotate_text(article_data['plaintext'])
    article_data['spotlight_json'] = spotlight_json
    article_repo.write_article(args.article_plaintexts_dir, title, article_data)

#filepaths_sanenames = []
#
#for root, subdirs, files in os.walk(args.article_plaintexts_dir):
#    for filename in files:
#        file_path = os.path.join(root, filename)
#
#        article_sanename = '.'.join(filename.split('.')[:-1])
#        filepaths_sanenames.append((file_path, article_sanename))
#
#filepaths_sanenames.sort()
#
#for file_path, article_sanename in filepaths_sanenames:
#    output_path = os.path.join(args.outputs_dir, article_sanename + '.spotlight.json')
#    if os.path.isfile(output_path):
#        print(article_sanename, "-- already annotated")
#        continue
#    else:
#        print(article_sanename)
#
#    text = open(file_path).read()
#    try:
#        result = spotlight.annotate_text(text)
#        queries += 1
#
#        with open(output_path, 'w') as f:
#            f.write(json.dumps(result))
#    except ValueError as e:
#        # TODO: BAD!
#        print('cannot process!')
#        print(e)
#
#    if args.max_queries >= 0 and queries >= args.max_queries:
#        print("max queries exceeded")
#        sys.exit(0)
#
#    time.sleep(args.sleep_between_queries)
