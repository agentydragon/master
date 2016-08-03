#!/bin/bash

set -e

# TODO: this is a bad hack :(
cd; cd bin
source common.sh

./metacentrum_spotlight.py \
	--article_plaintexts_dir=$WIKI_ARTICLES_PLAINTEXTS_DIR \
	--outputs_dir=$SPOTLIGHT_ANNOTATIONS_DIR \
	--max_queries=-1 \
	--sleep_between_queries=5
