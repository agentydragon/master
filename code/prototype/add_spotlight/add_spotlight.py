#!/usr/bin/python3

"""
Usage:
    bazel run :add_spotlight \
        --article=(...) \
        --article=(...)
"""

import sys
import time
import locale
locale.setlocale(locale.LC_ALL, 'en_US.utf8')

from py import paths

import argparse
parser = argparse.ArgumentParser(description='Look up articles in Spotlight')
parser.add_argument('--article_plaintexts_dir',
                    default=paths.WIKI_ARTICLES_PLAINTEXTS_DIR)
parser.add_argument('--articles', action='append')
parser.add_argument('--spotlight_endpoint')
args = parser.parse_args()

# TODO: skip if finished

import json
import os.path
from py import spotlight
from prototype import article_repo

if args.spotlight_endpoint:
    spotlight.SPOTLIGHT_SERVER = args.spotlight_endpoint

for title in args.articles:
    print("Spotlighting", title)
    article_data = article_repo.load_article(args.article_plaintexts_dir, title)

    # Skip if already done.
    if 'spotlight_json' in article_data:
        continue

    spotlight_json = spotlight.annotate_text(article_data['plaintext'])
    article_data['spotlight_json'] = spotlight_json
    article_repo.write_article(args.article_plaintexts_dir, title, article_data)
    print("Done")
