#!/bin/bash

source common.sh

echo "installing own code"

bazel build :metacentrum_get_training_samples
scp -r bazel-bin/metacentrum_get_training_samples* prvak@zuphux.metacentrum.cz:$BIN_ROOT

bazel build :metacentrum_add_negative_samples
scp -r bazel-bin/metacentrum_add_negative_samples* prvak@zuphux.metacentrum.cz:$BIN_ROOT

bazel build :metacentrum_distant_supervision_train
scp -r bazel-bin/metacentrum_distant_supervision_train* prvak@zuphux.metacentrum.cz:$BIN_ROOT

#FILES="\
#	annotate_coreferences.py \
#	annotate_coreferences.sh \
#	article_parse.py \
#	common.sh \
#	get_training_samples.py \
#	metacentrum_corenlp.sh \
#	metacentrum_download_dumps.sh \
#	metacentrum_get_training_samples.sh \
#	metacentrum_install_corenlp.sh \
#	metacentrum_prepare.sh \
#	metacentrum_split_wiki.sh \
#	metacentrum_spotlight.py \
#	metacentrum_spotlight.sh \
#	dbpedia.py \
#	wikidata.py \
#	sparql_client.py \
#	json_cache.py \
#	nlpize_articles.py \
#	nlpize_articles.sh \
#	parse_xmls_to_protos.py \
#	parse_xmls_to_protos.sh \
#	data_stats.sh \
#	split_wiki.py \
#	spotlight.py \
#	wiki2text \
#"

#scp $FILES prvak@zuphux.metacentrum.cz:$BIN_ROOT
