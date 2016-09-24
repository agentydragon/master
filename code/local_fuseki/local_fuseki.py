import paths
from thirdparty.fuseki import fuseki
import subprocess
import datetime
import os

scratch_dir = os.environ['SCRATCHDIR']

print("Copying Wikidata to local disk...", datetime.datetime.now())
rv = subprocess.call([
    "cp",
    "-rv",
    paths.WORK_DIR + '/fuseki-datasets/wikidata',
    scratch_dir + '/wikidata'
])
print("Copied.")
assert rv == 0

print("Copying DBpedia to local disk...", datetime.datetime.now())
rv = subprocess.call([
    "cp",
    "-rv",
    paths.WORK_DIR + '/fuseki-datasets/dbpedia-sameas',
    scratch_dir + '/dbpedia-sameas'
])
print("Copied.")
assert rv == 0

print("Starting Wikidata Fuseki...", datetime.datetime.now())
fuseki.spawn(
    dataset_path = scratch_dir + '/fuseki-datasets/wikidata',
    namespace = '/wikidata',
    port = 3030
)

print("Starting DBpedia Fuseki...", datetime.datetime.now())
fuseki.spawn(
    dataset_path = scratch_dir + '/fuseki-datasets/dbpedia-sameas',
    namespace = '/dbpedia-sameas',
    port = 3031
)

cmdline = [
    "prototype/make_training_samples/make_training_samples",
    "--wikidata_endpoint",
    "http://localhost:3030/wikidata/query",
    "--dbpedia_endpoint",
    "http://localhost:3031/dbpedia-sameas/query",
]

for article in ['George Washington', 'Albert Einstein', 'Adolf Hitler',
                'Charlie Chaplin', 'John Lennon']:
    args.extend(['--articles', article])

print(cmdline, datetime.datetime.now())
subprocess.call(cmdline)
