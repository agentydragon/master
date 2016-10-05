import subprocess
import os

def load_ttl_file(dataset_path, ttl_file_paths):
    commandline = [
        '../jena/apache-jena-3.1.0/bin/tdbloader2',
        '--loc',
        dataset_path
    ] + ttl_file_paths

    subprocess.call(commandline, env={
        'JVM_ARGS': '-Xmx22000M',
        'TMPDIR': os.environ['SCRATCHDIR']
    })
