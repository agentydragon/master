"""
Splits Wiki plaintext into articles.

Usage: TODO
"""

import io
import json
import locale
import datetime
locale.setlocale(locale.LC_ALL, 'en_US.utf8')

import re
from src.prototype.lib import article_repo
from src.prototype.lib import sentence

#from etaprogress.progress import ProgressBarBytes
import progressbar
import sys
import os

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

    total_size = os.stat(wiki_plaintext_path).st_size
    read = 0
    last_report = datetime.datetime.now()

    with io.open(wiki_plaintext_path, encoding='utf8') as f:
        articles = 0
        regex = re.compile('^= .+ =$')

        #bar = ProgressBarBytes(total_size, max_width=20)
        bar = progressbar.ProgressBar(widgets=[
            progressbar.Timer(), ' ',
            progressbar.Percentage(), ' ',
            progressbar.AdaptiveETA(), ' ',
            progressbar.Bar(),
        ], max_value = total_size, redirect_stdout=True)

        for line in f:
            read += len(line.encode('UTF-8'))
            # bar.numerator = read

            if regex.match(line):
                if articletitle is not None:
                    if article_repository.article_exists(articletitle):
                        message = articletitle + ' already exists'
                        pass
                    else:
                        message = 'writing: ' + articletitle
                        sys.stdout.flush()

                        articletext = sanitize_article(articletext)
                        article = sentence.SavedDocument(
                            plaintext = articletext,
                            title = articletitle,
                            corenlp_xml = None,
                            spotlight_json = None,

                            sentences = None,
                            coreferences = None,
                            spotlight_mentions = None,
                        )
                        article_repository.write_article(articletitle, article)
                    if (datetime.datetime.now() - last_report).seconds >= 5:
                        last_report = datetime.datetime.now()
                        print('#%d' % articles, message)
                        bar.update(read)
                        # print(('#%d' % articles + ' ' + message).ljust(40)[:40],
                        #       bar,
                        #       end='\r')
                        sys.stdout.flush()



                articletext = ""
                articletitle = line.strip().replace('= ', '').replace(' =', '')

                #print(line)
                articles += 1
                if target_articles is not None and articles > target_articles:
                    break
            #out.write(line)
            articletext += line
