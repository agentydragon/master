#!/bin/bash

set -e

# TODO: this is a bad hack :(
cd; cd bin
source common.sh

module add jdk-8

./metacentrum_nlpize_articles.py \
	--plaintexts_dir=$WIKI_ARTICLES_PLAINTEXTS_DIR \
	--output_parse_xmls_dir=$WIKI_ARTICLE_PARSES_DIR

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
