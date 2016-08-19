#!/bin/bash
#/home/prvak/master/corenlp-jar/stanford-corenlp-full-2015-12-09/corenlp.sh -file /mnt/crypto/data/wiki_small.txt
#/home/prvak/master/corenlp-jar/stanford-corenlp-full-2015-12-09/corenlp.sh -file /mnt/crypto/data/wiki-articles/Autism.txt

# finishes, is slow
/home/prvak/master/corenlp-jar/stanford-corenlp-full-2015-12-09/corenlp.sh \
	-file small_test \
	-annotators tokenize,ssplit,parse,lemma,ner,dcoref
	#-file /mnt/crypto/data/wiki-articles/Allan_Dwan.txt \
