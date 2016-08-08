#!/bin/bash

set -e

# Assumes CWD is ${RUNFILES}
# TODO

source common.sh

./add_negative_samples_main \
	--annotated_documents_dir $ANNOTATED_DOCUMENTS_DIR \
	--input_training_data $TRAINING_SAMPLES_FILE \
	--output_training_data $FULL_TRAINING_SAMPLES_FILE \
	--max_sentences=10000
	# --max_sentences=-1
