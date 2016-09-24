import paths
from thirdparty.fuseki import fuseki
import subprocess
import os

scratch_dir = os.environ['SCRATCHDIR']

print("Copying Wikidata to local disk...")
rv = subprocess.call([
    "cp",
    "-rv",
    paths.WORK_DIR + '/fuseki-datasets/wikidata',
    scratch_dir + '/wikidata'
])
print("Copied.")
assert rv == 0

print("Starting Fuseki...")
fuseki.serve_forever(
    dataset_path = scratch_dir + '/fuseki-datasets/wikidata',
    namespace = '/wikidata',
    port = 3030
)

# TODO
