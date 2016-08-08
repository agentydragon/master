#!/bin/bash

source common.sh

module add jdk-8
$CORENLP_RUNNER_SH $*
