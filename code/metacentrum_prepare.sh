#!/bin/bash

set -e

source common.sh

WIKIPEDIA_DUMP_DATE=20160720
WIKIPEDIA_DUMP_FILENAME=enwiki-${WIKIPEDIA_DUMP_DATE}-pages-articles.xml.bz2
WIKIPEDIA_DUMP_FILE=$WIKIPEDIA_DUMP_DIR/${WIKIPEDIA_DUMP_FILENAME}

function convert_wikipedia_to_plaintext() {
	echo "converting wikipedia to plaintext"
	# TODO: -done--file?
	bzcat $WIKIPEDIA_DUMP_FILE | $WIKI2TEXT_BINARY > $WIKIPEDIA_PLAINTEXT
}

function main() {
	./metacentrum_download_dumps.sh
	convert_wikipedia_to_plaintext
}

main
