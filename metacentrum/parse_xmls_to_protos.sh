#!/bin/bash

set -e

# TODO: this is a bad hack :(
cd; cd bin
source common.sh

./parse_xmls_to_protos.py \
	--plaintexts_dir $WIKI_ARTICLES_PLAINTEXTS_DIR \
	--parse_xmls_dir $WIKI_ARTICLE_PARSES_DIR \
	--outputs_dir $PARSE_PROTOS_DIR
