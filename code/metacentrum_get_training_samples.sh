#!/bin/bash

set -e

# Assumes CWD is ${RUNFILES}
# TODO

source common.sh

./get_training_samples_main \
	--annotated_documents_dir $ANNOTATED_DOCUMENTS_DIR \
	--output_file $TRAINING_SAMPLES_FILE \
	--intermediate_dir $TRAINING_SAMPLES_INTERMEDIATE_DIR \
	--max_documents=10
#	--max_documents=100
	# --max_sentences=-1
