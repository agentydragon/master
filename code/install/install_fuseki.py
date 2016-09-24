from thirdparty.jena import jena
from prototype.lib import file_util
import subprocess
import paths

dataset_path = paths.WORK_DIR + '/fuseki-datasets/wikidata'
file_util.ensure_dir(dataset_path)

# Load Wikidata triples.
print("loading...")
jena.load_ttl_file(
    dataset_path,
    ttl_file_path = paths.WIKIDATA_TTL_DUMP_UNPACKED_FILE
)
