#!/usr/bin/python3

"""
Usage:
    bazel run :add_spotlight \
        --article=(...) \
        --article=(...)
"""

import json
import os.path
from prototype.lib import spotlight
from prototype.lib import article_repo
import sys
import time
import locale
locale.setlocale(locale.LC_ALL, 'en_US.utf8')

from prototype.lib import flags
flags.add_argument('--articles', action='append')
flags.add_argument('--force_redo')
flags.make_parser(description='Look up articles in Spotlight')
args = flags.parse_args()

# TODO: skip if finished


spotlight_client = spotlight.SpotlightClient()
repo = article_repo.ArticleRepo()

for title in args.articles:
    print("Spotlighting", title)

    if not repo.article_exists(title):
        print("Doesn't exist")
        continue

    article_data = repo.load_article(title)

    # Skip if already done.
    if article_data.spotlight_json:
        if not args.force_redo:
            print("Already done")
            continue
    plaintext = article_data.plaintext
    if plaintext.strip() == '':
        print("Empty article")
        continue
    spotlight_json = spotlight_client.annotate_text(plaintext)
    article_data.spotlight_json = spotlight_json
    repo.write_article(title, article_data)
    print("Done")
