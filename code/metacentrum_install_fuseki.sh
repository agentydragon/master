#!/bin/bash

set -e

source common.sh

mkdir -p $FUSEKI_DIR
cd $FUSEKI_DIR

wget http://mirror.dkm.cz/apache/jena/binaries/apache-jena-3.1.0.tar.gz
wget http://mirror.dkm.cz/apache/jena/binaries/jena-fuseki-2.4.0.tar.gz
tar xvvfz apache-jena-3.1.0.tar.gz
tar xvvfz jena-fuseki-2.4.0.tar.gz
cd jena-fuseki-2.4.0
mkdir db
../apache-jena-3.1.0/bin/tdbloader2 --loc db ../2014/dbpedia_2014.owl ../2014/*.nt
