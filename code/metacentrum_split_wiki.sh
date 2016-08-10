#!/bin/bash

#  # Split wiki.
#  qsub -l walltime=24:00:00 -l nodes=1:brno:ppn=1,mem=1gb -m abe metacentrum_split_wiki.sh

set -e

cd $PBS_O_WORKDIR
source common.sh

mkdir -p $WIKI_ARTICLES_PLAINTEXTS_DIR
$BIN_ROOT/split_wiki.py \
	--max_articles=-1 \
	--target_dir=$WIKI_ARTICLES_PLAINTEXTS_DIR \
	--wiki_plaintext_path=$WIKIPEDIA_PLAINTEXT
