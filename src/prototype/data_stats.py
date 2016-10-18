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
with_proto = 0
fully_processed = []

repo = article_repo.ArticleRepo()

bar = progressbar.ProgressBar(capture_stdout=True)
for title in bar(art_set.article_names):
    if not repo.article_exists(title):
        nonexistant += 1
        continue

    art = repo.load_article(title)
    if art.plaintext:
        got_plaintext += 1
    if art.spotlight_json:
        with_spotlight += 1
    if art.corenlp_xml:
        with_corenlp += 1
    if art.sentences:
        with_proto += 1
    if art.spotlight_json and art.corenlp_xml and art.sentences:
        fully_processed.append(title)

print(
    "Nonexistant", nonexistant,
    "plaintext", got_plaintext,
    "spotlight", with_spotlight,
    "corenlp", with_corenlp,
    "proto", with_proto,
    "fully processed", len(fully_processed),
)
# for name in fully_processed:
#     print(name)
