#!/bin/bash

set -e

source common.sh

CORENLP_FN=stanford-corenlp-full-2015-12-09.zip
mkdir -p $CORENLP_DIR
CORENLP_ZIP_TARGET=$CORENLP_DIR/$CORENLP_FN
wget http://nlp.stanford.edu/software/stanford-corenlp-full-2015-12-09.zip -O$CORENLP_ZIP_TARGET
cd $CORENLP_DIR
unzip $CORENLP_FN

