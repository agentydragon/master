#!/bin/bash

set -e

source common.sh

mkdir -p $DBPEDIA_SPOTLIGHT_DIR
cd $DBPEDIA_SPOTLIGHT_DIR
wget http://spotlight.sztaki.hu/downloads/dbpedia-spotlight-latest.jar
wget http://spotlight.sztaki.hu/downloads/latest_models/en.tar.gz
tar xzf en.tar.gz
