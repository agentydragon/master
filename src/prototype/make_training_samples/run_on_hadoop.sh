#!/bin/bash
set -e
export HADOOP_CLASSPATH=$(hbase classpath):`pwd`/src/prototype/make_training_samples/MakeTrainingSamples_deploy.jar
hadoop jar `pwd`/src/prototype/make_training_samples/MakeTrainingSamples.jar \
	MakeTrainingSamples \
	-D mapreduce.map.memory.mb=9000 \
	-D mapred.child.java.opts=-Xmx8000m \
	-D mapreduce.map.java.opts='-Xmx8000m -XX:+UseParallelOldGC -XX:ParallelGCThreads=4' \
	-D wikidata_endpoint=http://hador:3030/merged/query \
	-D mapreduce.task.timeout=60000000 \
	-D hbase.client.retries.number=10 \
	-D hbase.client.scanner.timeout.period=600000000
