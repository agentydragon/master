#!/bin/bash

set -e

# source common.sh

module add jdk-8

/storage/brno3-cerit/home/prvak/fuseki/apache-jena-3.1.0/bin/tdbloader2 --loc /storage/brno7-cerit/home/prvak/data/fuseki-datasets/wikidata/ /storage/brno7-cerit/home/prvak/data/wikidata/wikidata-20160801-all-BETA.ttl
