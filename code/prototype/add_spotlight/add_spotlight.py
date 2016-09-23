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

import paths

import argparse
parser = argparse.ArgumentParser(description='Look up articles in Spotlight')
parser.add_argument('--article_plaintexts_dir')
parser.add_argument('--articles', action='append')
parser.add_argument('--spotlight_endpoint')
parser.add_argument('--force_redo')
args = parser.parse_args()

# TODO: skip if finished

import json
import os.path
from py import spotlight
from prototype.lib import article_repo

spotlight_client = spotlight.SpotlightClient(args.spotlight_endpoint)

for title in args.articles:
    print("Spotlighting", title)

    if not article_repo.article_exists(title,
                                       target_dir=args.article_plaintexts_dir):
        print("Doesn't exist")
        continue

    article_data = article_repo.load_article(args.article_plaintexts_dir, title)

    # Skip if already done.
    if ('spotlight_json' in article_data):
        if not args.force_redo:
            print("Already done")
            continue
    plaintext = article_data['plaintext']
    if plaintext.strip() == '':
        print("Empty article")
        continue
    spotlight_json = spotlight_client.annotate_text(plaintext)
    article_data['spotlight_json'] = spotlight_json
    article_repository = article_repo.ArticleRepo(args.article_plaintexts_dir)
    article_repo.write_article(title, article_data)
    print("Done")
