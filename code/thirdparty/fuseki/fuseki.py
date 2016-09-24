import os
from prototype.lib import pbs_util

def serve_forever(dataset_path, namespace):
    os.chdir('../jena_fuseki/apache-jena-fuseki-2.4.0')
    os.execv("/bin/bash", [
        "bash",
        "-c",
        ("./fuseki-server --loc " + dataset_path + " " + namespace),
    ])
