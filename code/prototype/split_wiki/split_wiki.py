#!/usr/bin/python

"""
Splits Wiki plaintext into articles.

Usage: TODO
"""

import io
import json
import locale
locale.setlocale(locale.LC_ALL, 'en_US.utf8')

import re
from prototype.lib import article_repo
from prototype.lib import sentence

# For workstation:
# WIKI_PLAINTEXT_FILE='/mnt/crypto/data/wiki.txt'
# TARGET_DIR='/mnt/crypto/data/wiki-articles'


#def get_article_corpus(target_articles):
#    with io.open('/mnt/crypto/data/wiki_small.txt', 'w') as out:
#        with io.open(WIKI_PLAINTEXT_FILE) as f:
#            articles = 0
#            regex = re.compile('^= .+ =$')
#            for line in f:
#                if regex.match(line):
#                    print(line)
#                    articles += 1
#                    if articles > target_articles:
#                        break
#                out.write(line)
#
#get_article_corpus(target_articles=1)

def remove_headings(article):
    regex = re.compile('^=+.+=+$', flags=re.MULTILINE)
    return re.sub(regex, '', article)

def sanitize_article(article):
    article = remove_headings(article)

    # TODO: remove References section?
    # TODO: use lists? (see Allan Dwan - list of movies)

    return article


def split_corpus(wiki_plaintext_path, target_articles=None):
    articletext = ""
    articletitle = None

    article_repository = article_repo.ArticleRepo()

    with io.open(wiki_plaintext_path, encoding='utf8') as f:
        articles = 0
        regex = re.compile('^= .+ =$')
        for line in f:
            if regex.match(line):
                if articletitle is not None:
                    if article_repository.article_exists(articletitle):
                        print('#%d' % articles, 'article', articletitle,
                              'already exists')
                        pass
                    else:
                        print('#%d' % articles, 'writing article:', articletitle)
                        articletext = sanitize_article(articletext)
                        article = sentence.SavedDocument(
                            plaintext = articletext,
                            title = articletitle,
                            corenlp_xml = None,
                            spotlight_json = None,
                            proto = None
                        )
                        article_repository.write_article(articletitle, article)

                articletext = ""
                articletitle = line.strip().replace('= ', '').replace(' =', '')

                #print(line)
                articles += 1
                if target_articles is not None and articles > target_articles:
                    break
            #out.write(line)
            articletext += line
