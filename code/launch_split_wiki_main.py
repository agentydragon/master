#!/usr/bin/python3

import pbs_util
import argparse
import file_util
import paths

parser = argparse.ArgumentParser(description='TODO')
parser.add_argument('--max_articles', default=-1, type=int)
parser.add_argument('--target_dir', default=paths.WIKI_ARTICLES_PLAINTEXTS_DIR)
parser.add_argument('--wiki_plaintext_path', default=paths.WIKIPEDIA_PLAINTEXT)
args = parser.parse_args()

file_util.ensure_dir(args.target_dir)

job_command = [
    # TODO: ???
    './split_wiki_main',
    '--max_articles',
    str(args.max_articles),
    '--target_dir',
    args.target_dir,
    '--wiki_plaintext_path',
    args.wiki_plaintext_path
]
pbs_util.launch_job(
    walltime="24:00:00",
    node_spec="nodes=1:brno:ppn=1,mem=4gb",
    job_name="wiki-split",
    job_command=job_command
)
