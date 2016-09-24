import subprocess

def load_ttl_file(dataset_path, ttl_file_path):
    subprocess.check_output([
        '../jena/apache-jena-3.1.0/bin/tdbloader2',
        '--loc',
        dataset_path,
        ttl_file_path
    ], stdout=subprocess.STDOUT)
