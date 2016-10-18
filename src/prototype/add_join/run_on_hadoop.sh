#!/bin/bash
set -e
export HADOOP_CLASSPATH=$(hbase classpath):`pwd`/src/prototype/add_join/AddJoin_deploy.jar
hadoop jar `pwd`/src/prototype/add_join/AddJoin.jar \
	AddJoin \
	-D dbpedia_endpoint=http://hador:3030/merged/query \
	-D mapreduce.task.timeout=60000000 \
	-D hbase.client.retries.number=10 \
	-D hbase.client.scanner.timeout.period=600000000
