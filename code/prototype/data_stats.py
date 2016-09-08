import article_repo
import argparse

from py import paths

parser = argparse.ArgumentParser(description='TODO')
parser.add_argument('--article_list_file', type=str, required=True)
parser.add_argument('--article_plaintexts_dir',
                    default=paths.WIKI_ARTICLES_PLAINTEXTS_DIR)
args = parser.parse_args()

with open(args.article_list_file) as f:
    article_names = list(map(lambda line: line.strip(), list(f)))

nonexistant = 0
got_plaintext = 0
fully_processed = []
for title in article_names:
    if not article_repo.article_exists(args.article_plaintexts_dir, title):
        nonexistant += 1

    art = article_repo.load_article(args.article_plaintexts_dir, title)
    if 'plaintext' in art:
        got_plaintext += 1
    if ('spotlight_json' in art) and ('corenlp_xml' in art):
        fully_processed.append(title)

print("Nonexistant", nonexistant,
      "With plaintext", got_plaintext,
      "Fully processed", len(fully_processed))
for name in fully_processed:
    print(name)
