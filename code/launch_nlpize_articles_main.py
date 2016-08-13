#!/usr/bin/python3

import argparse
import file_util
import paths
import os
import pbs_util

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
    if launched < args.max_launched_jobs:
        pbs_util.launch_job(
            walltime=str(slice_time),
    #        node_spec='nodes=1:ppn=1,mem=6gb',
            # 1 core is not enough
            node_spec='nodes=1:ppn=2,mem=6gb',
            job_name=job_name,
            job_command=job_command
        )
        launched += 1
    else:
        break
