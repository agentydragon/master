#!/bin/bash

set -e

source common.sh

echo "Plaintexts: `ls -R -1 $WIKI_ARTICLES_PLAINTEXTS_DIR | wc -l`"
echo "Parse XMLs: `ls -la $WIKI_ARTICLE_PARSES_DIR | wc -l`"
echo "Parse protos: `ls -la $PARSE_PROTOS_DIR | wc -l`"
echo
echo "Spotlights: `ls -la $SPOTLIGHT_ANNOTATIONS_DIR | wc -l`"
echo
echo "Annotated documents: `ls -la $ANNOTATED_DOCUMENTS_DIR | wc -l`"
