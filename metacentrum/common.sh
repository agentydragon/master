# TODO HAX
export LANG=en_US.UTF-8
export LANGUAGE=
export LC_CTYPE="en_US.UTF-8"
export LC_NUMERIC="en_US.UTF-8"
export LC_TIME="en_US.UTF-8"
export LC_COLLATE="en_US.UTF-8"
export LC_MONETARY="en_US.UTF-8"
export LC_MESSAGES="en_US.UTF-8"
export LC_PAPER="en_US.UTF-8"
export LC_NAME="en_US.UTF-8"
export LC_ADDRESS="en_US.UTF-8"
export LC_TELEPHONE="en_US.UTF-8"
export LC_MEASUREMENT="en_US.UTF-8"
export LC_IDENTIFICATION="en_US.UTF-8"
export LC_ALL=
# ^-- TODO HAX

STORAGE_NODE=brno3-cerit
STORAGE_ROOT=/storage/$STORAGE_NODE
STORAGE_HOME=$STORAGE_ROOT/home/prvak
BIN_ROOT=$STORAGE_HOME/bin
WIKI2TEXT_BINARY=$BIN_ROOT/wiki2text

CORENLP_DIR=$STORAGE_HOME/corenlp
CORENLP_RUNNER_SH=$CORENLP_DIR/stanford-corenlp-full-2015-12-09/corenlp.sh

WORK_DIR=$STORAGE_HOME/data
WIKIPEDIA_PLAINTEXT=$WORK_DIR/wiki-plain.txt

WIKI_ARTICLES_PLAINTEXTS_DIR=$WORK_DIR/wiki-articles-plaintexts
WIKI_ARTICLE_PARSES_DIR=$WORK_DIR/wiki-articles-parses
SPOTLIGHT_ANNOTATIONS_DIR=$WORK_DIR/spotlight-annotations
PARSE_PROTOS_DIR=$WORK_DIR/parse-protos
ANNOTATED_DOCUMENTS_DIR=$WORK_DIR/annotated-document-protos
SENTENCES_ENTITIES_DIR=$WORK_DIR/sentences-entities
TRAINING_SAMPLES_FILE=$WORK_DIR/training-samples.json

# FUSEKI_DIR=$STORAGE_HOME/fuseki
