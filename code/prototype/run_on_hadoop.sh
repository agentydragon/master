#!/bin/bash

set -e

bazel build :HBaseToJSON :HBaseToJSON_deploy.jar
BAZEL_BIN="$(pwd)/../bazel-bin"
export HADOOP_CLASSPATH=$(hbase classpath):$BAZEL_BIN/prototype/HBaseToJSON_deploy.jar

# TODO: hbase.client.max.perregion.tasks => is now 1. should set higher?

# Reduce memory?
hadoop jar $BAZEL_BIN/prototype/HBaseToJSON.jar \
	HBaseToJSON \
	-D java.security.auth.login.config=/storage/brno2/home/prvak/master/code/hadoop/jaas.conf
