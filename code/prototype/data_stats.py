from prototype.lib import article_repo
from prototype.lib import article_set
from prototype.lib import flags

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
