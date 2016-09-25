from prototype.lib import article_repo
from prototype.lib import article_set
from prototype.lib import flags

import sys
import progressbar
import paths

flags.make_parser(description='TODO')
args = flags.parse_args()

art_set = article_set.ArticleSet()

nonexistant = 0
got_plaintext = 0
with_spotlight = 0
with_corenlp = 0
fully_processed = []

repo = article_repo.ArticleRepo()

for title in art_set.article_names:
    if not repo.article_exists(title):
        nonexistant += 1
        continue

    art = repo.load_article(title)
    if art.plaintext:
        got_plaintext += 1
    if art.spotlight_json and art.corenlp_xml:
        fully_processed.append(title)
    if art.spotlight_json:
        with_spotlight += 1
    if art.corenlp_xml:
        with_corenlp += 1

print("Nonexistant", nonexistant,
      "With plaintext", got_plaintext,
      "With spotlight", with_spotlight,
      "With corenlp", with_corenlp,
      "Fully processed", len(fully_processed))
for name in fully_processed:
    print(name)
