from thirdparty.jena import jena
from prototype.lib import file_util
import subprocess
import paths

dataset_path = paths.WORK_DIR + '/fuseki-datasets/merged'

print("cleaning output")
subprocess.call([
    "rm",
    "-f",
    "interlanguage-links_en.ttl.bz2"
])
subprocess.call([
    "rm",
    "-f",
    "interlanguage-links_en.ttl"
])
subprocess.call([
    "rm",
    "-rf",
    dataset_path
])

file_util.ensure_dir(dataset_path)

print("downloading...")
subprocess.call([
    "wget",
    "http://downloads.dbpedia.org/2015-04/core-i18n/en/interlanguage-links_en.ttl.bz2"
])

print("bunzipping...")
subprocess.call([
    "bunzip2",
    "interlanguage-links_en.ttl.bz2"
])

# TODO: Needs lots of RAM and scratch space
print("loading...")
jena.load_ttl_file(
    dataset_path,
    ttl_file_paths=[paths.WIKIDATA_TTL_DUMP_FILE,
                    "interlanguage-links_en.ttl"]
)
