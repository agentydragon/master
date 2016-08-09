#!/bin/bash

set -e

source common.sh

cd $DBPEDIA_SPOTLIGHT_DIR
java -jar dbpedia-spotlight-latest.jar en http://localhost:2222/rest
