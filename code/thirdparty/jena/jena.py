import subprocess

def load_ttl_file(dataset_path, ttl_file_path):
    subprocess.call([
        '../jena/apache-jena-3.1.0/bin/tdbloader2',
        '--loc',
        dataset_path,
        ttl_file_path
    ])
