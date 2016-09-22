set -e

source paths.sh

function convert_wikipedia_to_plaintext() {
	echo "converting wikipedia to plaintext"
	# TODO: -done--file?
	bzcat $WIKIPEDIA_DUMP_FILE | ./wiki2text > $WIKIPEDIA_PLAINTEXT
}

function main() {
	#./metacentrum_download_dumps.sh
	convert_wikipedia_to_plaintext
}

main
