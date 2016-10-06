from prototype.kb import fuseki_config
from prototype.kb import fuseki
from prototype.lib import flags
import paths
import subprocess
import datetime
import os

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

# def destroy_dataset(dataset):
#     rv = subprocess.call([
#         "rm",
#         "-rf",
#         dataset
#     ])
#     print("Destroyed dataset", dataset)
#     assert rv == 0

scratch_dir = os.environ['SCRATCHDIR']
# scratch_dir = '/scratch/prvak'
wikidata_dataset = scratch_dir + '/wikidata'
dbpedia_sameas_dataset = scratch_dir + '/dbpedia-sameas'

def spawn_datasets():
    wikidata_dataset_source = paths.WORK_DIR + '/fuseki-datasets/wikidata'
    dbpedia_sameas_dataset_source = paths.WORK_DIR + '/fuseki-datasets/dbpedia-sameas'
    # wikidata_dataset = wikidata_dataset_source
    # dbpedia_sameas_dataset = dbpedia_sameas_dataset_source

    # donefile = '/scratch/prvak/datasets.copied'

    # if os.path.isfile(donefile):
    #     return

    copy_dataset(wikidata_dataset_source, wikidata_dataset,
                 name="Wikidata")
    copy_dataset(dbpedia_sameas_dataset_source, dbpedia_sameas_dataset,
                 name="DBpedia owl:sameAs")
    # assert subprocess.call(["touch", donefile]) == 0
    print('Datasets spawned.')

def main():
    flags.add_argument('--articles', action='append')
    flags.make_parser(description='TODO')
    args = flags.parse_args()

    spawn_datasets()

    print("Starting local Fuseki...", datetime.datetime.now())
    config_file_path = scratch_dir + '/fuseki-config.ttl'
    fuseki_config.write_config(config_file_path, wikidata_dataset, dbpedia_sameas_dataset)
    fuseki.spawn(
        config = config_file_path,
        port = 3030
    )

    cmdline = [
        "prototype/make_training_samples/make_training_samples",
        "--wikidata_endpoint",
        "http://localhost:3030/wikidata/query",
    ]

    for article in args.articles:
        cmdline.extend(['--articles', article])

    print(cmdline, datetime.datetime.now())
    rv = subprocess.call(cmdline)
    assert rv == 0

    # TODO: destroy datasets

if __name__ == '__main__':
    main()
