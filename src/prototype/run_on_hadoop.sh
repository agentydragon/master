#!/bin/bash
set -e
export HADOOP_CLASSPATH=$(hbase classpath):`pwd`/src/prototype/HBaseToJSON_deploy.jar
hadoop jar `pwd`/src/prototype/HBaseToJSON.jar HBaseToJSON
