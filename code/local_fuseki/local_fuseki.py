import paths
from thirdparty.fuseki import fuseki
from prototype.lib import flags
from local_fuseki import config
import subprocess
import datetime
import os

scratch_dir = os.environ['SCRATCHDIR']

wikidata_dataset_source = paths.WORK_DIR + '/fuseki-datasets/wikidata'
dbpedia_sameas_dataset_source = paths.WORK_DIR + '/fuseki-datasets/dbpedia-sameas'

def copy_dataset(dataset_from, dataset_to, name):
    print("Copying %s dataset to local disk..." % name, datetime.datetime.now())
    rv = subprocess.call([
        "cp",
        "-rv",
        dataset_from,
        dataset_to
    ])
    print("Copied.")
    assert rv == 0

# wikidata_dataset = wikidata_dataset_source
# dbpedia_sameas_dataset = dbpedia_sameas_dataset_source

wikidata_dataset = scratch_dir + '/wikidata'
dbpedia_sameas_dataset = scratch_dir + '/dbpedia-sameas'
copy_dataset(wikidata_dataset_source, wikidata_dataset,
             name="Wikidata")
copy_dataset(dbpedia_sameas_dataset_source, dbpedia_sameas_dataset,
             name="DBpedia owl:sameAs")

print("Starting Wikidata Fuseki...", datetime.datetime.now())
config_file_path = scratch_dir + '/fuseki-config.ttl'
config.write_config(config_file_path,
                    wikipedia_dataset, dbpedia_sameas_dataset)
fuseki.spawn(
    config = config_file_path,
    port = 3030
)

flags.add_argument('--articles', action='append')
flags.make_parser(description='TODO')
args = flags.parse_args()

cmdline = [
    "prototype/make_training_samples/make_training_samples",
    "--wikidata_endpoint",
    "http://localhost:3030/wikidata/query",
    "--dbpedia_endpoint",
    "http://localhost:3030/dbpedia-sameas/query",
]

for article in args.articles:
    cmdline.extend(['--articles', article])

print(cmdline, datetime.datetime.now())
subprocess.call(cmdline)
