#!/bin/bash

set -e

source paths.sh

module add jdk-8

wget http://downloads.dbpedia.org/2015-04/core-i18n/en/interlanguage-links_en.ttl.bz2
bunzip interlanguage-links_en.ttl.bz2

WD=$STORAGE_HOME/data/fuseki-datasets/dbpedia-sameas
mkdir -p $WD
../apache-jena-3.1.0/bin/tdbloader2 --loc $WD interlanguage-links_en.ttl
