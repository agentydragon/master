#!/bin/bash

set -e

source common.sh

module add jdk-8

cd $DBPEDIA_SPOTLIGHT_DIR
java -Xmx6g -jar dbpedia-spotlight-latest.jar en http://localhost:2222/rest
