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
from py import file_util
from prototype import article_repo

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


def split_corpus(wiki_plaintext_path, target_dir, target_articles=None):
    articletext = ""
    articletitle = None
    with io.open(wiki_plaintext_path, encoding='utf8') as f:
        articles = 0
        regex = re.compile('^= .+ =$')
        for line in f:
            if regex.match(line):
                if articletitle is not None:
                    if article_repo.article_exists(target_dir, articletitle):
                        print('#%d' % articles, 'article', articletitle,
                              'already exists')
                        pass
                    else
                        print('#%d' % articles, 'writing article:', articletitle)
                        articletext = sanitize_article(articletext)
                        article_repo.write_article(target_dir, articletitle,
                                                   {'title': articletitle, 'plaintext':
                                                    articletext})

                articletext = ""
                articletitle = line.strip().replace('= ', '').replace(' =', '')

                #print(line)
                articles += 1
                if target_articles is not None and articles > target_articles:
                    break
            #out.write(line)
            articletext += line
