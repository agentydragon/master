#!/usr/bin/python

"""
Splits Wiki plaintext into articles.

Usage:
    ./split_wiki.py \
        --max_articles=-1 \
        --target_dir=/storage/brno3-cerit/home/prvak/data/wiki-articles \
        --wiki_plaintext_path=/storage/brno3-cerit/home/prvak/data/wiki-plain.txt
"""

import argparse

parser = argparse.ArgumentParser(description='Split plaintext Wiki into articles')
parser.add_argument('--max_articles', type=int)
parser.add_argument('--target_dir', type=str)
parser.add_argument('--wiki_plaintext_path', type=str)
args = parser.parse_args()

import re

# For workstation:
# WIKI_PLAINTEXT_FILE='/mnt/crypto/data/wiki.txt'
# TARGET_DIR='/mnt/crypto/data/wiki-articles'

import os
if not os.path.isdir(args.target_dir):
    os.makedirs(args.target_dir)

#def get_article_corpus(target_articles):
#    with open('/mnt/crypto/data/wiki_small.txt', 'w') as out:
#        with open(WIKI_PLAINTEXT_FILE) as f:
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

def article_title_to_path(title):
    sanitized_articletitle = title.replace(' ', '_')
    first1 = sanitized_articletitle[:1]
    first2 = sanitized_articletitle[:2]
    target_dir = args.target_dir + '/' + first1 + '/' + first2
    if not os.path.isdir(target_dir):
        os.makedirs(target_dir)
    return target_dir + '/' + sanitized_articletitle + '.txt'

def split_corpus(target_articles=None):
    articletext = ""
    articletitle = None
    with open(args.wiki_plaintext_path) as f:
        articles = 0
        regex = re.compile('^= .+ =$')
        for line in f:
            if regex.match(line):
                if articletitle is not None:
                    path = article_title_to_path(articletitle)
                    with open(path, 'w') as out:
                        print('Writing article: ' + articletitle)
                        articletext = sanitize_article(articletext)
                        out.write(articletext)

                articletext = ""
                articletitle = line.strip().replace('= ', '').replace(' =', '')

                #print(line)
                articles += 1
                if target_articles is not None and articles > target_articles:
                    break
            #out.write(line)
            articletext += line

if args.max_articles >= 1:
    split_corpus(target_articles=args.max_articles)
else:
    split_corpus()
