import json
import os.path
from src.prototype.lib import article_repo
from src.prototype.lib import dbpedia
import sys
import time
import locale
locale.setlocale(locale.LC_ALL, 'en_US.utf8')

from src.prototype.lib import flags
flags.add_argument('--articles', action='append')
flags.make_parser()
args = flags.parse_args()

repo = article_repo.ArticleRepo()
dbpedia_client = dbpedia.DBpediaClient()

for title in args.articles:
    print("Joining", title)

    if not repo.article_exists(title):
        print("Doesn't exist")
        continue

    document = repo.load_article(title)
    if not document.corenlp_xml:
        print("Not parsed yet")
        continue
    if not document.spotlight_json:
        print("Not Spotlighted yet")
        continue
    # Skip if already done.
    plaintext = document.plaintext
    if plaintext.strip() == '':
        print("Empty article")
        continue
    document.add_proto_to_document(dbpedia_client = dbpedia_client)
    repo.write_article(title, document)
    print("Done")
