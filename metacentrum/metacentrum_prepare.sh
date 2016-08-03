#!/bin/bash

set -e

source common.sh

WIKIPEDIA_DUMP_DIR=$WORK_DIR/wikipedia_dump
WIKIPEDIA_DUMP_DATE=20160720
WIKIPEDIA_DUMP_FILENAME=enwiki-${WIKIPEDIA_DUMP_DATE}-pages-articles.xml.bz2
WIKIPEDIA_DUMP_FILE=$WIKIPEDIA_DUMP_DIR/${WIKIPEDIA_DUMP_FILENAME}
WIKIDATA_DUMP_DATE=20160801
WIKIDATA_DUMP_FILENAME=wikidata-${WIKIDATA_DUMP_DATE}-all.json.bz2
WIKIDATA_DUMP_FILE=$WORK_DIR/wikidata/${WIKIDATA_DUMP_FILENAME}

function download_wikipedia_dump() {
	echo "downloading wikipedia dump"
	mkdir -p $WIKIPEDIA_DUMP_DIR
	WIKIPEDIA_DUMP_URL=https://dumps.wikimedia.org/enwiki/$WIKIPEDIA_DUMP_DATE/$WIKIPEDIA_DUMP_FILENAME
	wget $WIKIPEDIA_DUMP_URL -O$WIKIPEDIA_DUMP_FILE --no-verbose --show-progress --continue
}

function download_wikidata_dump() {
	echo "downloading wikidata dump"
	mkdir -p $WORK_DIR/wikidata
	WIKIDATA_DUMP_URL=https://dumps.wikimedia.org/wikidatawiki/entities/$WIKIDATA_DUMP_DATE/$WIKIDATA_DUMP_FILENAME
	wget $WIKIDATA_DUMP_URL -O$WIKIDATA_DUMP_FILE --no-verbose --show-progress --continue
}

function convert_wikipedia_to_plaintext() {
	echo "converting wikipedia to plaintext"
	# TODO: -done--file?
	bzcat $WIKIPEDIA_DUMP_FILE | $WIKI2TEXT_BINARY > $WIKIPEDIA_PLAINTEXT
}

function main() {
	download_wikipedia_dump
	download_wikidata_dump
	convert_wikipedia_to_plaintext
}

main
