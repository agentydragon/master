#!/bin/bash

source common.sh

echo "installing own code"

FILES=wiki2text \
	common.sh \
	metacentrum_prepare.sh \
	metacentrum_install_corenlp.sh \
	metacentrum_corenlp.sh \
	split_wiki.py \


scp $FILES prvak@zuphux.metacentrum.cz:$STORAGE_HOME
