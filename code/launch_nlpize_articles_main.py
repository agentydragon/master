#!/usr/bin/python3

import sys
import argparse
import subprocess
import file_util
import paths
import os

parser = argparse.ArgumentParser(description='TODO')
parser.add_argument('--plaintexts_dir',
                    default=paths.WIKI_ARTICLES_PLAINTEXTS_DIR)
parser.add_argument('--job_count', type=int,
                    required=True)
parser.add_argument('--max_launched_jobs', type=int,
                    required=True)
parser.add_argument('--output_parse_xmls_dir',
                    default=paths.WIKI_ARTICLE_PARSES_DIR)
parser.add_argument('--time_per_article',
                    type=int,
                    # default=100)
                    default=300)  # 5 minutes (should be more or less OK)
args = parser.parse_args()

file_util.ensure_dir(args.output_parse_xmls_dir)

plaintext_paths = []
for root, subdirs, files in os.walk(args.plaintexts_dir):
    for filename in files:
        article_sanename = '.'.join(filename.split('.')[:-1])
        output_file = args.output_parse_xmls_dir + '/' + article_sanename + '.txt.out'
        if os.path.isfile(output_file):
            # done, skip
            continue

        # TODO: uninsanize
        if "'" in article_sanename or '"' in article_sanename or '$' in article_sanename:
            continue

        plaintext_path = os.path.join(root, filename)
        plaintext_paths.append(plaintext_path)

slice_size = len(plaintext_paths) / args.job_count
launched = 0
for i in range(0, len(plaintext_paths), slice_size):
    path_slice = plaintext_paths[i:i+slice_size]
    job_command = [
        # TODO: ???
        './nlpize_articles_main',
        '--output_parse_xmls_dir',
        args.output_parse_xmls_dir,
        '--parallel_runs',
        '1',
    ]
    for path in path_slice:
        job_command.extend(['--plaintext_files', "'" + path + "'"])
    # 30 seconds per article
    slice_time = args.time_per_article * len(path_slice)
    job_name = 'nlpize-articles-js-%d' % launched
    # NOTE: java heap has 5g in corenlp.sh, give some more.
    qsub_command = ['qsub',
                    '-l', 'walltime=' + str(slice_time),
    #                '-l', 'nodes=1:ppn=2,mem=6gb',
                    '-l', 'nodes=1:ppn=1,mem=6gb',
                    '-m', 'abe',
                    '-N', job_name]
    # qsub_command.append(' '.join(job_command))
    print(qsub_command)
    # print(' '.join(qsub_command))
    if launched < args.max_launched_jobs:
        job_script = ("""
#!/bin/bash
module add jdk-8

cd $PBS_O_WORKDIR
""" + (' '.join(job_command)))

        js_path = job_name + '.sh'
        with open(js_path, 'w') as jobscript_file:
            jobscript_file.write(job_script)
        print(job_script)

        qsub_command.append(js_path)
        popen = subprocess.Popen(qsub_command,
                                 #stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        stdoutdata, stderrdata = popen.communicate()#job_script)
        print(stdoutdata)
        print(stderrdata)
        if popen.returncode != 0:
            print(popen.returncode)
            sys.exit(1)
        launched += 1
    else:
        break
