#!/bin/bash

source common.sh

echo "installing own code"

FILES="wiki2text \
	common.sh \
	metacentrum_prepare.sh \
	metacentrum_install_corenlp.sh \
	metacentrum_corenlp.sh \
	metacentrum_split_wiki.sh \
	metacentrum_nlpize_articles.sh \
	split_wiki.py \
	spotlight.py \
	metacentrum_spotlight.sh \
	metacentrum_spotlight.py"

scp $FILES prvak@zuphux.metacentrum.cz:$BIN_ROOT
