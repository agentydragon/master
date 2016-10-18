#!/bin/bash

set -e

bazel build :AddJoin :AddJoin_deploy.jar
BAZEL_BIN="$(pwd)/../../bazel-bin"
export HADOOP_CLASSPATH=$(hbase classpath):$BAZEL_BIN/prototype/add_join/AddJoin_deploy.jar

# Reduce memory?
hadoop jar $BAZEL_BIN/prototype/add_join/AddJoin.jar \
	AddJoin \
	-D dbpedia_endpoint=http://hador:3030/merged/query \
	-D mapreduce.task.timeout=60000000 \
	-D hbase.client.retries.number=10 \
	-D hbase.client.scanner.timeout.period=600000000
