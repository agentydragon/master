#!/usr/bin/python

"""
Splits Wiki plaintext into articles.

Usage: TODO
"""

import json
import io
import locale
locale.setlocale(locale.LC_ALL, 'en_US.utf8')

import re
from py import file_util

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

import unicodedata
def sanitize_articletitle(title):
    sanitized_articletitle = title.replace(' ', '_').replace('/', '_')
    return sanitized_articletitle

def article_title_to_path(target_dir, title):
    sanitized_articletitle = sanitize_articletitle(title)
    first1 = sanitized_articletitle[:1]
    first2 = sanitized_articletitle[:2]
    first3 = sanitized_articletitle[:3]
    target_dir = target_dir + '/' + first1 + '/' + first2 + '/' + first3
    file_util.ensure_dir(target_dir)
    return target_dir + '/' + sanitized_articletitle + '.json'

def split_corpus(wiki_plaintext_path, target_dir, target_articles=None):
    articletext = ""
    articletitle = None
    with io.open(wiki_plaintext_path, encoding='utf8') as f:
        articles = 0
        regex = re.compile('^= .+ =$')
        for line in f:
            if regex.match(line):
                if articletitle is not None:
                    path = article_title_to_path(target_dir, articletitle)
                    with io.open(path, 'w', encoding='utf8') as out:
                        print('#%d' % articles, 'writing article:', articletitle)
                        articletext = sanitize_article(articletext)
                        json.dump({'title': articletitle, 'plaintext':
                                   articletext}, out)

                articletext = ""
                articletitle = line.strip().replace('= ', '').replace(' =', '')

                #print(line)
                articles += 1
                if target_articles is not None and articles > target_articles:
                    break
            #out.write(line)
            articletext += line
