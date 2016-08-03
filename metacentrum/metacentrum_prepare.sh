#!/bin/bash

# 1) copy wiki2text to /storage/brno7/home/prvak/wiki2text

WORK_DIR=/storage/brno7/home/prvak/data
WIKIPEDIA_DUMP_DIR=$WORK_DIR/wikipedia_dump
WIKIPEDIA_DUMP_DATE=20160720
WIKIPEDIA_DUMP_FILENAME=enwiki-${DUMP_DATE}-pages-articles.xml.bz2
WIKIPEDIA_DUMP_FILE=$WIKIPEDIA_DUMP_DIR/$DUMP_FILENAME
WIKIDATA_DUMP_FILE=$WORK_DIR/wikidata/latest-all.json.bz2
WIKIPEDIA_PLAINTEXT=$WORK_DIR/wiki-plain.txt

function download_wikipedia_dump() {
	mkdir -p $WIKIPEDIA_DUMP_DIR
	wget https://dumps.wikimedia.org/enwiki/$WIKIPEDIA_DUMP_DATE/$WIKIPEDIA_DUMP_FILENAME -O$WIKIPEDIA_DUMP_FILE
}

function download_wikidata_dump() {
	mkdir -p $WORK_DIR/wikidata
	wget https://dumps.wikimedia.org/wikidatawiki/entities/latest-all.json.bz2 -O$WIKIDATA_DUMP_FILE
}

function convert_wikipedia_to_plaintext() {
	WIKI2TEXT=/storage/brno7/home/prvak/wiki2text
	bzcat $WIKIPEDIA_DUMP_FILE | $WIKI2TEXT > $WIKIPEDIA_PLAINTEXT
}

function main() {
	download_wikipedia_dump
	download_wikidata_dump
	convert_wikipedia_to_plaintext
}

main
