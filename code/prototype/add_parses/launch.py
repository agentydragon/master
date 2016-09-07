from py import pbs_util
import argparse
import subprocess

parser = argparse.ArgumentParser(description='TODO')
parser.add_argument('--article_list_file', type=str, required=True)
parser.add_argument('--max_articles', type=int)
args = parser.parse_args()

with open(args.article_list_file) as f:
    article_names = list(map(lambda line: line.strip(), list(f)))

if args.max_articles:
    article_names = article_names[:args.max_articles]

# fails to run Java on remote machines :(

job_command = [
    'prototype/add_parses/add_parses',
] + article_names

#subprocess.check_output(job_command)

job_id = pbs_util.launch_job(
    # TODO: calculate walltime; parallelize
    walltime="01:00:00",
    node_spec="nodes=1:brno:ppn=4,mem=8gb",
    job_name="add-parses",
    job_command=job_command
)
print("Launched add-parses:", job_id)
