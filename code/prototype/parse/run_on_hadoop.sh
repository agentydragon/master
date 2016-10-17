#!/bin/bash

set -e

bazel build :CoreNLP.jar :CoreNLP_deploy.jar
BAZEL_BIN="$(pwd)/../../bazel-bin"
export HADOOP_CLASSPATH=$(hbase classpath):$BAZEL_BIN/prototype/parse/CoreNLP_deploy.jar

# TODO: hbase.client.max.perregion.tasks => is now 1. should set higher?

# Reduce memory?
hadoop jar $BAZEL_BIN/prototype/parse/CoreNLP.jar \
	CoreNLP \
	-D java.security.auth.login.config=/storage/brno2/home/prvak/master/code/hadoop/jaas.conf \
	-D mapreduce.map.memory.mb=9000 \
	-D mapred.job.map.memory.mb=9000 \
	-D mapred.child.java.opts=-Xmx8000m \
	-D mapreduce.map.java.opts='-Xmx8000m -XX:+UseParallelOldGC -XX:ParallelGCThreads=4' \
	-D mapreduce.task.timeout=60000000 \
	-D hbase.client.retries.number=10 \
	-D hbase.client.scanner.timeout.period=600000000 \
	-D mapreduce.map.maxattempts=1 \
	-D prefix_length=-1
	#-D prefix_length=100
	# timeout of scanner: 100 minutes (should be enough to parse anything)

# TODO: unlimited length prefixes

#	-Dmapred.job.map.memory.mb=5300 \
#	-Dmapred.child.java.opts="-Xmx5g" \
