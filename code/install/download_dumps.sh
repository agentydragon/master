#!/bin/bash

set -e

source paths.sh

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

	# TODO: bzcat only if needed

	echo "bunzipping ttl dump (this will take a long time, 67 gigs incoming)"
	bunzip2 $WIKIDATA_TTL_DUMP_FILE # XXX: > $WIKIDATA_TTL_DUMP_UNPACKED_FILE
}

function main() {
	download_wikipedia_dump
	download_wikidata_dump
}

main
