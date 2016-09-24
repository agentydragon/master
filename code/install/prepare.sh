#!/bin/bash

set -e

pwd
ls -la
echo
echo XXXXX
echo
cat paths.sh
echo
source paths.sh

function convert_wikipedia_to_plaintext() {
	echo "converting wikipedia to plaintext"
	# TODO: -done--file?
	bzcat $WIKIPEDIA_DUMP_FILE | ./wiki2text > $WIKIPEDIA_PLAINTEXT
}

function main() {
	convert_wikipedia_to_plaintext
}

main
