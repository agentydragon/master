import json
import os.path
from prototype.lib import parse_xmls_to_protos
from prototype.lib import article_repo
import sys
import time
import locale
locale.setlocale(locale.LC_ALL, 'en_US.utf8')

from prototype.lib import flags
flags.add_argument('--articles', action='append')
args = flags.parse_args()

repo = article_repo.ArticleRepo()

for title in args.articles:
    print("Spotlighting", title)

    if not repo.article_exists(title):
        print("Doesn't exist")
        continue

    article_data = repo.load_article(title)
    if not article_data.corenlp_xmls:
        print("Not parsed yet")
        continue
    if not article_data.spotlight_json:
        print("Not Spotlighted yet")
        continue
    # Skip if already done.
    plaintext = article_data.plaintext
    if plaintext.strip() == '':
        print("Empty article")
        continue
    proto = parse_xmls_to_protos.document_to_proto(
        title = title,
        document = article
    )
    article_data.proto = proto
    repo.write_article(title, article_data)
    print("Done")
