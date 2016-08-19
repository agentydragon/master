#!/bin/bash

# This script should run on a developer machine.

set -e

source common.sh

echo "installing own code"

function metacentrum_rm() {
	ssh zuphux.metacentrum.cz rm $*
}

function install_binary() {
	BINARY=$1
	metacentrum_rm -rf $BIN_ROOT/$1 $BIN_ROOT/$1.runfiles $BIN_ROOT/$1.runfiles_manifest
	bazel build :$1
	# scp -r bazel-bin/$1 bazel-bin/$1.runfiles bazel-bin/$1.runfiles_manifest prvak@zuphux.metacentrum.cz:$BIN_ROOT
	rsync -ar bazel-bin/$1 bazel-bin/$1.runfiles bazel-bin/$1.runfiles_manifest prvak@zuphux.metacentrum.cz:$BIN_ROOT
}

#install_binary annotate_coreferences
#install_binary metacentrum_add_negative_samples
#install_binary metacentrum_distant_supervision_train
#install_binary metacentrum_spotlight_main
#install_binary launch_get_training_samples_main
#install_binary launch_nlpize_articles_main
#install_binary launch_split_wiki_main

function install_jar() {
	# metacentrum_rm rm -rf $BIN_ROOT/${1}.jar
	bazel build hadoop:${1}.jar
	rsync -arv --progress bazel-bin/hadoop/${1}.jar prvak@zuphux.metacentrum.cz:$BIN_ROOT
}

install_jar WikiSplit_deploy
# XXX
install_jar CoreNLP_deploy
install_jar CoreNLP

FILES="\
	common.sh \
	data_stats.sh \
	metacentrum_install_dbpedia_spotlight.sh \
	metacentrum_run_spotlight.sh \
	metacentrum_install_fuseki.sh \
	wikidata_into_fuseki.sh \
"
#	metacentrum_corenlp.sh \
#	metacentrum_download_dumps.sh \
#	metacentrum_prepare.sh \
#	dbpedia.py \
#	wikidata.py \
#	wiki2text \

scp $FILES prvak@zuphux.metacentrum.cz:$BIN_ROOT
