STORAGE_NODE="brno3-cerit"
STORAGE_ROOT="/storage/" + STORAGE_NODE
STORAGE_HOME=STORAGE_ROOT + "/home/prvak"
BIN_ROOT=STORAGE_HOME + "/bin"
WIKI2TEXT_BINARY=BIN_ROOT + "/wiki2text"

CORENLP_DIR=STORAGE_HOME + "/corenlp"
CORENLP_RUNNER_SH=CORENLP_DIR + "/stanford-corenlp-full-2015-12-09/corenlp.sh"

WORK_DIR=STORAGE_HOME + "/data"
WIKIPEDIA_PLAINTEXT=WORK_DIR + "/wiki-plain.txt"

WIKI_ARTICLES_PLAINTEXTS_DIR=WORK_DIR + "/wiki-articles-plaintexts"
WIKI_ARTICLE_PARSES_DIR=WORK_DIR + "/wiki-articles-parses"
SPOTLIGHT_ANNOTATIONS_DIR=WORK_DIR + "/spotlight-annotations"
PARSE_PROTOS_DIR=WORK_DIR + "/parse-protos"
ANNOTATED_DOCUMENTS_DIR=WORK_DIR + "/annotated-document-protos"
TRAINING_SAMPLES_FILE=WORK_DIR + "/training-samples.pb"

JSON_CACHE_DIR = WORK_DIR + '/json-caches'
