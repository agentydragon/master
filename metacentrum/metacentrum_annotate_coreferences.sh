#!/bin/bash

set -e

# TODO: this is a bad hack :(
cd; cd bin
source common.sh

./metacentrum_annotate_coreferences.py \
	--input_protos_dir $PARSE_PROTOS_DIR \
	--spotlight_dir $SPOTLIGHT_ANNOTATIONS_DIR \
	--output_protos_dir $ANNOTATED_DOCUMENTS_DIR
