#!/bin/bash
set -e
export HADOOP_CLASSPATH=$(hbase classpath):`pwd`/src/prototype/make_training_samples/MakeTrainingSamples_deploy.jar
hadoop jar `pwd`/src/prototype/make_training_samples/MakeTrainingSamples.jar \
	MakeTrainingSamples \
	-D wikidata_endpoint=http://hador:3030/merged/query \
	-D hbase.client.retries.number=10 \
	-D hbase.client.scanner.timeout.period=600000000
