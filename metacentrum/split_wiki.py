#!/usr/bin/python

import re

# For workstation:
# WIKI_PLAINTEXT_FILE='/mnt/crypto/data/wiki.txt'
# TARGET_DIR='/mnt/crypto/data/wiki-articles'

# For metacentrum:
WIKI_PLAINTEXT_FILE='/storage/brno3-cerit/home/prvak/data/wiki-plain.txt'
TARGET_DIR='/storage/brno3-cerit/home/prvak/data/wiki-articles'

import os
os.makedirs(TARGET_DIR)

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

def split_corpus(target_articles):
    articletext = ""
    articletitle = None
    with open(WIKI_PLAINTEXT_FILE) as f:
        articles = 0
        regex = re.compile('^= .+ =$')
        for line in f:
            if regex.match(line):
                if articletitle is not None:
                    sanitized_articletitle = articletitle.replace(' ', '_')
                    with open(TARGET_DIR + '/' + sanitized_articletitle + '.txt', 'w') as out:
                        print('Writing article: ' + articletitle)
                        articletext = sanitize_article(articletext)
                        out.write(articletext)

                articletext = ""
                articletitle = line.strip().replace('= ', '').replace(' =', '')

                #print(line)
                articles += 1
                if articles > target_articles:
                    break
            #out.write(line)
            articletext += line

split_corpus(target_articles=100)
