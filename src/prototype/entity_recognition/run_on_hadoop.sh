#!/bin/bash

set -e

echo "SERVERS: [$1]"
# e.g.: http://hador:2222/rest/annotate

if [ -z $1 ]; then
	echo "No servers given!"
	exit 1
fi

export HADOOP_CLASSPATH=$(hbase classpath):`pwd`/src/prototype/entity_recognition/SpotlightAnnotator_deploy.jar

# TODO: hbase.client.max.perregion.tasks => is now 1. should set higher?

hadoop jar `pwd`/src/prototype/entity_recognition/SpotlightAnnotator.jar \
	SpotlightAnnotator \
	-D hbase.client.retries.number=10 \
	-D hbase.client.scanner.timeout.period=6000000 \
	-D spotlight_server=$1
