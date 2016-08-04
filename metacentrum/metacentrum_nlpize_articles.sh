#!/bin/bash

# per 1 instance: 5 GB RAM
# so, for 8 instances: 48 GB RAM

# 8 CPUs
# 48 GB RAM

set -e

# TODO: this is a bad hack :(
cd; cd bin
source common.sh

module add jdk-8

./metacentrum_nlpize_articles.py \
	--plaintexts_dir=$WIKI_ARTICLES_PLAINTEXTS_DIR \
	--output_parse_xmls_dir=$WIKI_ARTICLE_PARSES_DIR \
	--parallel_runs=16

#for ARTICLE_FILE in $WIKI_ARTICLES_PLAINTEXTS_DIR/*/*/*.txt; do
#	echo `date +%Y%m%d-%H%M`: "$ARTICLE_FILE"
#
#	# TODO: skip if output file already exists
#
#	# TODO: batch this!
#	$CORENLP_RUNNER_SH \
#		-file "$ARTICLE_FILE" \
#		-annotators tokenize,ssplit,parse,lemma,ner,dcoref \
#		-outputDirectory $WIKI_ARTICLE_PARSES_DIR
#
#	# saves: from ArticleName.txt -> ArticleName.txt.out
#done
