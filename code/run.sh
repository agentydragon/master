#!/bin/bash
module add jdk-8
module add python34-modules-gcc
cd /storage/brno7-cerit/home/prvak/master/code
/storage/brno7-cerit/home/prvak/bin/bazel run --script_path $SCRATCHDIR/script.sh spotlight:Spotlight
source $SCRATCHDIR/script.sh
