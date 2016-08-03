#!/bin/bash

set -e

# TODO: this is a bad hack :(
cd; cd bin
source common.sh

./metacentrum_get_sentences_entities.py \
	--plaintexts_dir $WIKI_ARTICLES_PLAINTEXTS_DIR \
	--parse_xmls_dir $WIKI_ARTICLE_PARSES_DIR \
	--spotlight_jsons_dir $SPOTLIGHT_ANNOTATIONS_DIR \
	--outputs_dir $SENTENCES_ENTITIES_DIR
