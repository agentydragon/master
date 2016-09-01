#!/usr/bin/python3

"""
Splits Wiki plaintext into articles.

Usage: TODO
"""

import file_util
import split_wiki
import argparse

def main():
    parser = argparse.ArgumentParser(description='Split plaintext Wiki into articles')
    parser.add_argument('--max_articles', type=int)
    parser.add_argument('--target_dir', type=str)
    parser.add_argument('--wiki_plaintext_path', type=str)
    args = parser.parse_args()
    file_util.ensure_dir(args.target_dir)
    if args.max_articles >= 1:
        split_wiki.split_corpus(args.wiki_plaintext_path, args.target_dir, target_articles=args.max_articles)
    else:
        split_wiki.split_corpus(args.wiki_plaintext_path, args.target_dir)

if __name__ == '__main__':
    main()
