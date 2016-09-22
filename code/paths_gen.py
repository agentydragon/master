#!/usr/bin/python

import argparse
parser = argparse.ArgumentParser(description='TODO')
parser.add_argument('--python_out', required=True)
parser.add_argument('--sh_out', required=True)
args = parser.parse_args()

# Generates paths.py and paths.sh.

storage_node = "brno7-cerit"
storage_root = "/storage/" + storage_node
storage_home = storage_root + "/home/prvak"

work_dir = storage_home + "/data"
wikipedia_plaintext = work_dir + "/wiki-plain.txt"
wiki_articles_plaintexts_dir = work_dir + "/wiki-articles-plaintexts"
log_path = storage_home + "/logs"
charts_path = storage_home + "/charts"
models_path = storage_home + "/models"

python = open(args.python_out, "w")
shell = open(args.sh_out, "w")

python.write(
    'WIKIPEDIA_PLAINTEXT = "' + wikipedia_plaintext + '"\n' +
    'WIKI_ARTICLES_PLAINTEXTS_DIR = "' + wiki_articles_plaintexts_dir+ '"\n' +
    'LOG_PATH = "' + log_path + '"\n' +
    'CHARTS_PATH = "' + charts_path + '"\n' +
    'MODELS_PATH = "' + models_path + '"\n' +
    ''
)

shell.write(
    'WIKIPEDIA_PLAINTEXT="' + wikipedia_plaintext + '"\n' +
    'WIKI_ARTICLES_PLAINTEXTS_DIR="' + wiki_articles_plaintexts_dir+ '"\n' +
    'LOG_PATH="' + log_path + '"\n' +
    'CHARTS_PATH="' + charts_path + '"\n' +
    'MODELS_PATH="' + models_path + '"\n' +
    '\n' +
    'STORAGE_HOME="' + storage_home + '"\n' +
    'WORK_DIR="' + work_dir + '"\n' +
    'FUSEKI_DIR="' + (storage_home + '/fuseki') + '"\n' +
    'WIKIDATA_DUMP_DIR="' + (work_dir + '/wikidata') + '"\n' +
    'WIKIDATA_DUMP_DATE="20160801"\n' +
    'WIKIDATA_TTL_DUMP_FILENAME=wikidata-${WIKIDATA_DUMP_DATE}-all-BETA.ttl.bz2\n' +
    'WIKIDATA_TTL_DUMP_FILE=$WIKIDATA_DUMP_DIR/${WIKIDATA_TTL_DUMP_FILENAME}\n' +
    'WIKIDATA_TTL_DUMP_UNPACKED_FILENAME=wikidata-${WIKIDATA_DUMP_DATE}-all-BETA.ttl.bz2\n' +
    'WIKIDATA_TTL_DUMP_UNPACKED_FILE=$WIKIDATA_DUMP_DIR/${WIKIDATA_TTL_DUMP_UNPACKED_FILENAME}\n' +
    ''
)

python.close()
shell.close()
# WIKI2TEXT_BINARY=BIN_ROOT + "/wiki2text"
