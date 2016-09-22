import paths

import os

os.chdir('../jena_fuseki/apache-jena-fuseki-2.4.0')
os.execv("/bin/bash", [
    "bash",
    "-c",
    ("./fuseki-server --loc " + paths.WORK_DIR +
     "/fuseki-datasets/wikidata /wikidata"),
])
