#!/bin/bash

set -e

# Assumes CWD is ${RUNFILES}
# TODO

source common.sh

./get_training_samples_main \
	--annotated_documents_dir $ANNOTATED_DOCUMENTS_DIR \
	--output_file $TRAINING_SAMPLES_FILE \
	--max_sentences=1000
	# --max_sentences=-1
