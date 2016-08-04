#!/bin/bash

source common.sh

echo "installing own code"

FILES="\
	common.sh \
	metacentrum_corenlp.sh \
	metacentrum_download_dumps.sh \
	metacentrum_install_corenlp.sh \
	nlpize_articles.sh \
	nlpize_articles.py \
	metacentrum_get_training_samples.sh \
	metacentrum_get_training_samples.py \
	get_training_samples.py \
	article_parse.py \
	metacentrum_prepare.sh \
	metacentrum_split_wiki.sh \
	metacentrum_spotlight.py \
	metacentrum_spotlight.sh \
	myutil.py \
	split_wiki.py \
	spotlight.py \
	sentence_pb2.py \
	training_samples_pb2.py \
	metacentrum_parse_xmls_to_protos.py \
	annotate_coreferences.py \
	annotate_coreferences.sh \
	metacentrum_parse_xmls_to_protos.sh \
	wiki2text \
"

scp $FILES prvak@zuphux.metacentrum.cz:$BIN_ROOT
