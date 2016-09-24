from thirdparty.jena import jena
from prototype.lib import file_util
import subprocess

dataset_path = paths.WORK_DIR + '/fuseki-datasets/dbpedia-sameas'

print("cleaning output")
subprocess.check_output([
    "rm",
    "-f",
    "interlanguage-links_en.ttl.bz2"
])
subprocess.check_output([
    "rm",
    "-f",
    "interlanguage-links_en.ttl"
])
subprocess.check_output([
    "rm",
    "-rf",
    dataset_path
])

file_util.ensure_dir(dataset_path)

print("downloading...")
subprocess.check_output([
    "wget",
    "http://downloads.dbpedia.org/2015-04/core-i18n/en/interlanguage-links_en.ttl.bz2"
], stdout=subprocess.STDOUT)

print("bunzipping...")
subprocess.check_output([
    "bunzip2 interlanguage-links_en.ttl.bz2"
], stdout=subprocess.STDOUT)

print("loading...")
jena.load_ttl_file(
    dataset_path,
    ttl_file_path="interlanguage-links_en.ttl"
)
