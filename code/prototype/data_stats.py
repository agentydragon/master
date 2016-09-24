from prototype.lib import article_repo
from prototype.lib import article_set
import argparse

import paths

parser = argparse.ArgumentParser(description='TODO')
parser.add_argument('--max_articles', type=int, default=None)
parser.add_argument('--article_list_file', default=None)
parser.add_argument('--article_plaintexts_dir')
args = parser.parse_args()

art_set = article_set.ArticleSet(
    path = args.article_list_file,
    maximum = args.max_articles
)

nonexistant = 0
got_plaintext = 0
with_spotlight = 0
with_corenlp = 0
fully_processed = []
for title in art_set.article_names:
    if not article_repo.article_exists(title,
                                       target_dir=args.article_plaintexts_dir):
        nonexistant += 1
        continue

    art = article_repo.load_article(args.article_plaintexts_dir, title)
    if 'plaintext' in art:
        got_plaintext += 1
    if ('spotlight_json' in art) and ('corenlp_xml' in art):
        fully_processed.append(title)
    if 'spotlight_json' in art:
        with_spotlight += 1
    if 'corenlp_xml' in art:
        with_corenlp += 1

print("Nonexistant", nonexistant,
      "With plaintext", got_plaintext,
      "With spotlight", with_spotlight,
      "With corenlp", with_corenlp,
      "Fully processed", len(fully_processed))
for name in fully_processed:
    print(name)
