import article_repo
import argparse

from py import paths

parser = argparse.ArgumentParser(description='TODO')
parser.add_argument('--max_articles', type=int)
parser.add_argument('--article_list_file', type=str, required=True)
parser.add_argument('--article_plaintexts_dir',
                    default=paths.WIKI_ARTICLES_PLAINTEXTS_DIR)
args = parser.parse_args()

with open(args.article_list_file) as f:
    article_names = list(map(lambda line: line.strip(), list(f)))

if args.max_articles:
    article_names = article_names[:args.max_articles]

nonexistant = 0
got_plaintext = 0
with_spotlight = 0
with_corenlp = 0
fully_processed = []
for title in article_names:
    if not article_repo.article_exists(args.article_plaintexts_dir, title):
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
