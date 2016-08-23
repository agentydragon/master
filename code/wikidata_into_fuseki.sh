#!/bin/bash

set -e

# source common.sh

module add jdk-8

export JVM_ARGS=-Xmx5000M
# orig: phase = all
/storage/brno7-cerit/home/prvak/fuseki/apache-jena-3.1.0/bin/tdbloader2 --phase index --loc /storage/brno7-cerit/home/prvak/data/fuseki-datasets/wikidata/ /storage/brno7-cerit/home/prvak/data/wikidata/wikidata-20160801-all-BETA.ttl
