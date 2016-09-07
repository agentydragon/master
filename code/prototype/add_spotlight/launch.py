from py import pbs_util
import argparse

parser = argparse.ArgumentParser(description='TODO')
parser.add_argument('--article_list_file', type=str, required=True)
parser.add_argument('--max_articles', type=int)
parser.add_argument('--spotlight_endpoint')
args = parser.parse_args()

with open(args.article_list_file) as f:
    article_names = list(map(lambda line: line.strip(), list(f)))

if args.max_articles:
    article_names = article_names[:args.max_articles]

job_command = [
    'prototype/add_spotlight/add_spotlight',
]

if args.spotlight_endpoint:
    job_command.extend(['--spotlight_endpoint', args.spotlight_endpoint])

print(article_names)
for name in article_names:
    job_command.append('--articles')
    job_command.append(name)

job_id = pbs_util.launch_job(
    # TODO: calculate walltime; parallelize
    walltime="01:00:00",
    node_spec="nodes=1:brno:ppn=1,mem=1gb",
    job_name="add-spotlight",
    job_command=job_command
)
print("Launched add-spotlight:", job_id)
