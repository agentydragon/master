from py import pbs_util
import argparse

parser = argparse.ArgumentParser(description='TODO')
parser.add_argument('--article_list_file', type=str, required=True)
args = parser.parse_args()

with open(args.article_list_file) as f:
    article_names = list(f)

job_command = [
    'prototype/add_parses/add_parses',
] + article_names
job_id = pbs_util.launch_job(
    # TODO: calculate walltime; parallelize
    walltime="01:00:00",
    node_spec="nodes=1:brno:ppn=1,mem=8gb",
    job_name="add-parses",
    job_command=job_command
)
print("Launched add-parses:", job_id)
