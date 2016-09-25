#!/usr/bin/python3

"""
Splits Wiki plaintext into articles.

Usage: TODO
"""

from prototype.lib import file_util
from prototype.split_wiki import split_wiki
from prototype.lib import flags

def main():
    flags.add_argument('--max_articles', type=int)
    flags.add_argument('--article_plaintexts_path', type=str)
    flags.add_argument('--wiki_plaintext_path', type=str, required=True)
    flags.make_parser(description='Split plaintext Wiki into articles')
    args = flags.parse_args()
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
