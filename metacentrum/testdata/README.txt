Base: Obama.txt
Derived by CoreNLP: Obama.txt.out
Derived by Spotlight: Obama.spotlight.json

./spotlight.py --article_plaintext_path=testdata/Obama.txt --output_path=testdata/Obama.spotlight.json
../../corenlp-jar/stanford-corenlp-full-2015-12-09/corenlp.sh \
	-file Obama.txt \
	-annotators tokenize,ssplit,parse,lemma,ner,dcoref
