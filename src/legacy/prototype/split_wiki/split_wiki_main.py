"""
Splits Wiki plaintext into articles.

Usage: TODO
"""

from src.prototype.split_wiki import split_wiki
from src.prototype.lib import flags

def main():
    flags.add_argument('--max_articles', type=int)
    flags.add_argument('--wiki_plaintext_path', type=str, required=True)
    flags.make_parser(description='Split plaintext Wiki into articles')
    args = flags.parse_args()
    if args.max_articles:
        split_wiki.split_corpus(args.wiki_plaintext_path,
                                target_articles=args.max_articles)
    else:
        split_wiki.split_corpus(args.wiki_plaintext_path)

if __name__ == '__main__':
    main()
