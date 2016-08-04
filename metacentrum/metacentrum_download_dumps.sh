#!/bin/bash

set -e

source common.sh

WIKIPEDIA_DUMP_DIR=$WORK_DIR/wikipedia_dump
WIKIPEDIA_DUMP_DATE=20160720
WIKIPEDIA_DUMP_FILENAME=enwiki-${WIKIPEDIA_DUMP_DATE}-pages-articles.xml.bz2
WIKIPEDIA_DUMP_FILE=$WIKIPEDIA_DUMP_DIR/${WIKIPEDIA_DUMP_FILENAME}

WIKIDATA_DUMP_DIR=$WORK_DIR/wikidata
WIKIDATA_DUMP_DATE=20160801
WIKIDATA_JSON_DUMP_FILENAME=wikidata-${WIKIDATA_DUMP_DATE}-all.json.bz2
WIKIDATA_JSON_DUMP_FILE=$WIKIDATA_DUMP_DIR/${WIKIDATA_JSON_DUMP_FILENAME}
WIKIDATA_TTL_DUMP_FILENAME=wikidata-${WIKIDATA_DUMP_DATE}-all-BETA.ttl.bz2
WIKIDATA_TTL_DUMP_FILE=$WIKIDATA_DUMP_DIR/${WIKIDATA_TTL_DUMP_FILENAME}

function download_wikipedia_dump() {
	echo "downloading wikipedia dump"
	mkdir -p $WIKIPEDIA_DUMP_DIR
	WIKIPEDIA_DUMP_URL=https://dumps.wikimedia.org/enwiki/$WIKIPEDIA_DUMP_DATE/$WIKIPEDIA_DUMP_FILENAME
	wget $WIKIPEDIA_DUMP_URL -O$WIKIPEDIA_DUMP_FILE --no-verbose --show-progress --continue
}

function download_wikidata_dump() {
	echo "downloading wikidata dump"
	mkdir -p $WORK_DIR/wikidata
	echo "downloading json dump"
	WIKIDATA_JSON_DUMP_URL=https://dumps.wikimedia.org/wikidatawiki/entities/$WIKIDATA_DUMP_DATE/$WIKIDATA_JSON_DUMP_FILENAME
	wget $WIKIDATA_JSON_DUMP_URL -O$WIKIDATA_JSON_DUMP_FILE --no-verbose --show-progress --continue

	echo "downloading ttl dump"
	WIKIDATA_TTL_DUMP_URL=https://dumps.wikimedia.org/wikidatawiki/entities/$WIKIDATA_DUMP_DATE/$WIKIDATA_TTL_DUMP_FILENAME
	wget $WIKIDATA_TTL_DUMP_URL -O$WIKIDATA_TTL_DUMP_FILE --no-verbose --show-progress --continue
}

function main() {
	download_wikipedia_dump
	download_wikidata_dump
}

main
