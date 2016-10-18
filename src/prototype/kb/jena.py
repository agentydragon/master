import subprocess
import os

def load_ttl_file(dataset_path, ttl_file_paths):
    commandline = [
        '../jena/apache-jena-3.1.0/bin/tdbloader2',
        # '--sort-args',
        # ('"--buffer-size=40G ' + #--temporary-directory=' + os.environ['SCRATCHDIR'] + ' '
        #   '--parallel=4"'),
        '--jvm-args',
        ('-Xmx30000M'),
        '--loc',
        dataset_path
    ] + ttl_file_paths
    print(commandline)

    env = dict(os.environ)
    # env['JVM_ARGS'] = '-Xmx100000M'
    env['JVM_ARGS'] = '-Xmx30000M'
    env['TMPDIR'] = os.environ['SCRATCHDIR']
    subprocess.call(commandline, env=env)
