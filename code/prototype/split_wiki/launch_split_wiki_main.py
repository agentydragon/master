#!/usr/bin/python3

from py import pbs_util
from py import file_util
from py import paths
import argparse

parser = argparse.ArgumentParser(description='TODO')
parser.add_argument('--max_articles', type=int, required=True)
parser.add_argument('--target_dir', default=paths.WIKI_ARTICLES_PLAINTEXTS_DIR)
parser.add_argument('--wiki_plaintext_path', default=paths.WIKIPEDIA_PLAINTEXT)
args = parser.parse_args()

file_util.ensure_dir(args.target_dir)

job_command = [
    'prototype/split_wiki/split_wiki_main',
    '--max_articles',
    str(args.max_articles),
    '--target_dir',
    args.target_dir,
    '--wiki_plaintext_path',
    args.wiki_plaintext_path
]
job_id = pbs_util.launch_job(
    walltime="00:01:00",
    node_spec="nodes=1:brno:ppn=1,mem=4gb",
    job_name="wiki-split",
    job_command=job_command
)
print("Launched wiki split:", job_id)
