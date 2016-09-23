import argparse
parser = argparse.ArgumentParser(description='TODO')
parser.add_argument('--python_out', required=True)
parser.add_argument('--sh_out', required=True)
parser.add_argument('--java_out', required=True)
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

# Dump dates
wikidata_dump_date = '20160801'
wikipedia_dump_date = '20160720'

relation_samples_dir = work_dir + '/relation-samples'

python = open(args.python_out, "w")
shell = open(args.sh_out, "w")
java = open(args.java_out, "w")

python.write(
    'WIKIPEDIA_PLAINTEXT = "' + wikipedia_plaintext + '"\n'
    'WIKI_ARTICLES_PLAINTEXTS_DIR = "' + wiki_articles_plaintexts_dir+ '"\n'
    'RELATION_SAMPLES_DIR = "' + relation_samples_dir + '"\n'
    'WORK_DIR = "' + work_dir + '"\n'
    'LOG_PATH = "' + log_path + '"\n'
    'CHARTS_PATH = "' + charts_path + '"\n'
    'MODELS_PATH = "' + models_path + '"\n'
    '\n'
    # TODO: hack
    'ARTICLE_LIST_PATH = "' + (storage_home + "/master/code/prototype/persons") + '"\n'
    # TODO: allow path overrides
)

wikidata_dump_dir = (work_dir + '/wikidata')
shell.write(
    'WIKIPEDIA_PLAINTEXT="' + wikipedia_plaintext + '"\n'
    '\n'
    'STORAGE_HOME="' + storage_home + '"\n'
    'WORK_DIR="' + work_dir + '"\n'
    'FUSEKI_DIR="' + (storage_home + '/fuseki') + '"\n'
    'WIKIDATA_DUMP_DATE="' + wikidata_dump_date + '"\n'
    'WIKIDATA_TTL_DUMP_FILENAME=wikidata-${WIKIDATA_DUMP_DATE}-all-BETA.ttl.bz2\n'
    'WIKIDATA_TTL_DUMP_FILE=' + wikidata_dump_dir + '/${WIKIDATA_TTL_DUMP_FILENAME}\n'
    'WIKIDATA_TTL_DUMP_UNPACKED_FILENAME=wikidata-${WIKIDATA_DUMP_DATE}-all-BETA.ttl.bz2\n'
    'WIKIDATA_TTL_DUMP_UNPACKED_FILE=' + wikidata_dump_dir + '/${WIKIDATA_TTL_DUMP_UNPACKED_FILENAME}\n'
    'WIKIPEDIA_DUMP_DIR="' + (work_dir + '/wikipedia_dump') + '"\n'
    'WIKIPEDIA_DUMP_DATE="' + wikipedia_dump_date + '"\n'
    'WIKIPEDIA_DUMP_FILENAME=enwiki-${WIKIPEDIA_DUMP_DATE}-pages-articles.xml.bz2\n'
    'WIKIPEDIA_DUMP_FILE=$WIKIPEDIA_DUMP_DIR/${WIKIPEDIA_DUMP_FILENAME}\n'
    'WIKIDATA_JSON_DUMP_FILENAME=wikidata-${WIKIDATA_DUMP_DATE}-all.json.bz2\n'
    'WIKIDATA_JSON_DUMP_FILE=' + wikidata_dump_dir + '/${WIKIDATA_JSON_DUMP_FILENAME}\n'
    ''
)

java.write("""
    public class Paths {
        public static String RelationSamplesDir = \"""" + relation_samples_dir + """\";
        public static String WikiArticlesPlaintextsDir = \"""" + wiki_articles_plaintexts_dir + """\";
    }
""")

python.close()
shell.close()
java.close()
