#!/bin/bash

set -e

source paths.sh

module add jdk-8

mkdir -p $FUSEKI_DIR
cd $FUSEKI_DIR

wget http://mirror.dkm.cz/apache/jena/binaries/apache-jena-3.1.0.tar.gz
tar xvvfz apache-jena-3.1.0.tar.gz
rm apache-jena-3.1.0.tar.gz

WD=$STORAGE_HOME/data/fuseki-datasets/wikidata
mkdir -p $WD

# Load Wikidata triples.
../apache-jena-3.1.0/bin/tdbloader2 --loc $WD $WIKIDATA_TTL_DUMP_UNPACKED_FILE
