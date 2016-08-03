#!/bin/bash

source common.sh

module add jdk-8

for ARTICLE_FILE in $WIKI_ARTICLES_PLAINTEXTS_DIR/*/*/*.txt; do
	echo `date +%Y%m%d-%H%M`: "$ARTICLE_FILE"

	# TODO: batch this!
	$CORENLP_RUNNER_SH \
		-file "$ARTICLE_FILE" \
		-annotators tokenize,ssplit,parse,lemma,ner,dcoref \
		-outputDirector $WIKI_ARTICLE_PARSE_DIR

	# saves: from ArticleName.txt -> ArticleName.txt.out
done
