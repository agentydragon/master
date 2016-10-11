#!/bin/bash

bazel build :WikiSplit_deploy.jar
BAZEL_BIN="$(pwd)/../../bazel-bin"
export HADOOP_CLASSPATH=$(hbase classpath):$BAZEL_BIN/prototype/split_wiki/WikiSplit_deploy.jar
hadoop jar $BAZEL_BIN/prototype/split_wiki/WikiSplit_deploy.jar \
	-Djava.security.auth.login.config=/storage/brno2/home/prvak/master/code/hadoop/jaas.conf \
	/user/prvak/wiki-plain/wiki-plain.txt
