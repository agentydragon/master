#!/bin/bash
export HADOOP_CLASSPATH=$(hbase classpath):`pwd`/src/prototype/split_wiki/WikiSplit_deploy.jar
hadoop jar `pwd`/src/prototype/split_wiki/WikiSplit_deploy.jar \
	/user/prvak/wiki-plain/wiki-plain.txt
