#!/usr/bin/python3

"""
Splits Wiki plaintext into articles.

Usage: TODO
"""

from py import file_util
from prototype.split_wiki import split_wiki
import argparse

def main():
    parser = argparse.ArgumentParser(description='Split plaintext Wiki into articles')
    parser.add_argument('--max_articles', type=int)
    parser.add_argument('--article_plaintexts_path', type=str)
    parser.add_argument('--wiki_plaintext_path', type=str, required=True)
    args = parser.parse_args()
    file_util.ensure_dir(args.article_plaintexts_path)
    if args.max_articles >= 1:
        split_wiki.split_corpus(args.wiki_plaintext_path,
                                args.article_plaintexts_path,
                                target_articles=args.max_articles)
    else:
        split_wiki.split_corpus(args.wiki_plaintext_path,
                                args.article_plaintexts_path)

if __name__ == '__main__':
    main()
