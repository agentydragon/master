import paths

import os

os.execv("/bin/bash", [
    "apache-jena-fuseki-2.4.0/fuseki-server",
    "--loc",
    paths.WORK_DIR + "/fuseki-datasets/wikidata",
    "/wikidata",
])
