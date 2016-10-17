#!/bin/bash

set -e

echo "SERVERS: [$1]"

if [ -z $1 ]; then
	echo "No servers given!"
	exit 1
fi

bazel build :SpotlightAnnotator.jar :SpotlightAnnotator_deploy.jar
BAZEL_BIN="$(pwd)/../../bazel-bin"
export HADOOP_CLASSPATH=$(hbase classpath):$BAZEL_BIN/prototype/entity_recognition/SpotlightAnnotator_deploy.jar

# TODO: hbase.client.max.perregion.tasks => is now 1. should set higher?

# Reduce memory?
hadoop jar $BAZEL_BIN/prototype/entity_recognition/SpotlightAnnotator.jar \
	SpotlightAnnotator \
	-D java.security.auth.login.config=/storage/brno2/home/prvak/master/code/hadoop/jaas.conf \
	-D mapreduce.map.memory.mb=1000 \
	-D mapred.job.map.memory.mb=1000 \
	-D mapred.child.java.opts=-Xmx800m \
	-D mapreduce.map.java.opts='-Xmx800m -XX:+UseParallelOldGC -XX:ParallelGCThreads=4' \
	-D mapreduce.task.timeout=600000 \
	-D hbase.client.retries.number=10 \
	-D hbase.client.scanner.timeout.period=6000000 \
	-D mapreduce.map.maxattempts=1 \
	-D spotlight_server=$1
