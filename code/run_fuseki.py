import paths

import os

dataset_path = paths.WORK_DIR + '/fuseki-datasets/wikidata'

os.chdir('../jena_fuseki/apache-jena-fuseki-2.4.0')
os.execv("/bin/bash", [
    "bash",
    "-c",
    ("./fuseki-server --loc " + dataset_path + " /wikidata"),
])
