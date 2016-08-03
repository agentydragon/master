#!/bin/bash

set -e

# TODO: this is a bad hack :(
cd; cd bin
source common.sh

./metacentrum_get_training_samples.py \
	--sentences_entities_dir $SENTENCES_ENTITIES_DIR \
	--output_file $TRAINING_SAMPLES_FILE
