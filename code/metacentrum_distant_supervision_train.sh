#!/bin/bash

set -e

# Assumes CWD is ${RUNFILES}
# TODO

source common.sh

./distant_supervision_train_main \
	--training_data $TRAINING_SAMPLES_FILE
#	--training_data $FULL_TRAINING_SAMPLES_FILE
