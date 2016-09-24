#!/usr/bin/python3

from prototype.lib import pbs_util
from prototype.lib import file_util
import paths
import argparse

parser = argparse.ArgumentParser(description='TODO')
parser.add_argument('--max_articles', type=int, required=True)
parser.add_argument('--article_plaintexts_dir')
parser.add_argument('--wiki_plaintext_path', default=paths.WIKIPEDIA_PLAINTEXT)
args = parser.parse_args()

file_util.ensure_dir(args.article_plaintexts_dir)

job_command = [
    'prototype/split_wiki/split_wiki_main',
    '--max_articles',
    str(args.max_articles),
    '--article_plaintexts_dir',
    args.article_plaintexts_dir,
    '--wiki_plaintext_path',
    args.wiki_plaintext_path
]
job_id = pbs_util.launch_job(
    walltime="48:00:00",
    node_spec="nodes=1:brno:ppn=2,mem=4gb",
    job_name="wiki-split",
    job_command=job_command
)
print("Launched wiki split:", job_id)
