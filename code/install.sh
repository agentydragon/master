#!/bin/bash

set -e

source common.sh

echo "installing own code"

function install_binary() {
	BINARY=$1
	ssh-metacentrum rm -rf bin/$1 bin/$1.runfiles bin/$1.runfiles_manifest
	bazel build :$1
	scp -r bazel-bin/$1 bazel-bin/$1.runfiles bazel-bin/$1.runfiles_manifest prvak@zuphux.metacentrum.cz:$BIN_ROOT
}

install_binary annotate_coreferences
install_binary metacentrum_get_training_samples
install_binary metacentrum_add_negative_samples
install_binary metacentrum_distant_supervision_train
install_binary metacentrum_spotlight_main

FILES="\
	common.sh \
	data_stats.sh \
"
#	annotate_coreferences.py \
#	annotate_coreferences.sh \
#	article_parse.py \
#	metacentrum_corenlp.sh \
#	metacentrum_download_dumps.sh \
#	metacentrum_install_corenlp.sh \
#	metacentrum_prepare.sh \
#	metacentrum_split_wiki.sh \
#	dbpedia.py \
#	wikidata.py \
#	sparql_client.py \
#	json_cache.py \
#	nlpize_articles.py \
#	nlpize_articles.sh \
#	parse_xmls_to_protos.py \
#	parse_xmls_to_protos.sh \
#	split_wiki.py \
#	spotlight.py \
#	wiki2text \

scp $FILES prvak@zuphux.metacentrum.cz:$BIN_ROOT
