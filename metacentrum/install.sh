#!/bin/bash

source common.sh

echo "installing own code"

FILES="\
	common.sh \
	metacentrum_corenlp.sh \
	metacentrum_install_corenlp.sh \
	metacentrum_nlpize_articles.sh \
	metacentrum_nlpize_articles.py \
	metacentrum_get_sentences_entities.py \
	metacentrum_get_sentences_entities.sh \
	article_parse.py \
	metacentrum_prepare.sh \
	metacentrum_split_wiki.sh \
	metacentrum_spotlight.py \
	metacentrum_spotlight.sh \
	myutil.py \
	split_wiki.py \
	spotlight.py \
	wiki2text \
"

scp $FILES prvak@zuphux.metacentrum.cz:$BIN_ROOT
