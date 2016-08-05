#!/bin/bash

set -e

# TODO: this is a bad hack :(
cd; cd bin
source common.sh

./metacentrum_get_training_samples.py \
	--annotated_documents_dir $ANNOTATED_DOCUMENTS_DIR \
	--output_file $TRAINING_SAMPLES_FILE \
	--max_sentences=-1
	#--max_sentences=1000
