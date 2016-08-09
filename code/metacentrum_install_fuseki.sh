#!/bin/bash

set -e

source common.sh

module add jdk-8

mkdir -p $FUSEKI_DIR
cd $FUSEKI_DIR

wget http://mirror.dkm.cz/apache/jena/binaries/apache-jena-3.1.0.tar.gz
wget http://mirror.dkm.cz/apache/jena/binaries/apache-jena-fuseki-2.4.0.tar.gz
tar xvvfz apache-jena-3.1.0.tar.gz
tar xvvfz apache-jena-fuseki-2.4.0.tar.gz
rm apache-jena-3.1.0.tar.gz
rm apache-jena-fuseki-2.4.0.tar.gz

chmod +x apache-jena-fuseki-2.4.0/fuseki-server

WD=$STORAGE_HOME/data/fuseki-datasets/wikidata
mkdir -p $WD

# Load Wikidata triples.
../apache-jena-3.1.0/bin/tdbloader2 --loc $WD $WIKIDATA_TTL_DUMP_UNPACKED_FILE
# alternative way to put in all wikidata:
#bin/s-put http://localhost:3030/wikidata/data default $WIKIDATA_TTL_DUMP_UNPACKED_FILE

cd apache-jena-fuseki-2.4.0
./fuseki-server --loc $WD /wikidata    # --update
