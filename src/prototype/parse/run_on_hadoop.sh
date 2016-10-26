#!/bin/bash
set -e
export HADOOP_CLASSPATH=$(hbase classpath):`pwd`/src/prototype/parse/CoreNLP_deploy.jar
# TODO: hbase.client.max.perregion.tasks => is now 1. should set higher?
hadoop jar `pwd`/src/prototype/parse/CoreNLP.jar \
	CoreNLP \
	-D mapred.child.java.opts=-Xmx8000m \
	-D mapreduce.tasktracker.map.tasks.maximum=8 \
	-D mapreduce.map.cpu.vcores=4 \
	-D hbase.client.retries.number=10 \
	-D hbase.client.scanner.timeout.period=600000000 \
	-D prefix_length=-1
	# (2016-10-26): 6 GB is not enough
	#-D prefix_length=100
	# timeout of scanner: 100 minutes (should be enough to parse anything)

# TODO: unlimited length prefixes

#	-Dmapred.job.map.memory.mb=5300 \
#	-Dmapred.child.java.opts="-Xmx5g" \
