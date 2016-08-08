#!/bin/bash

set -e

source common.sh

mkdir -p $WIKI_ARTICLES_PLAINTEXTS_DIR
$BIN_ROOT/split_wiki.py \
	--max_articles=-1 \
	--target_dir=$WIKI_ARTICLES_PLAINTEXTS_DIR \
	--wiki_plaintext_path=$WIKIPEDIA_PLAINTEXT
