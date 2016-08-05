#!/bin/bash

set -e

../spotlight.py --article_plaintext_path=Obama.txt --output_path=Obama.spotlight.json
../../corenlp-jar/stanford-corenlp-full-2015-12-09/corenlp.sh \
	-file Obama.txt \
	-annotators tokenize,ssplit,parse,lemma,ner,dcoref
