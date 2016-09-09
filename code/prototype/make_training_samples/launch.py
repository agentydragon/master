#!/usr/bin/python3

from py import pbs_util
import argparse
import subprocess

def launch_job_for_slice(articles_slice, wikidata_endpoint):
    job_command = ['prototype/make_training_samples/make_training_samples']
    if wikidata_endpoint:
        job_command.extend(['--wikidata_endpoint', wikidata_endpoint])
    for article in articles_slice:
        job_command.extend(['--articles', article])
    job_id = pbs_util.launch_job(
        # TODO: calculate walltime; parallelize
        walltime="04:00:00",
        node_spec="nodes=1:brno:ppn=2,mem=2gb",
        job_name="make-training-samples",
        job_command=job_command
    )
    print("Launched add-parses:", job_id)

def main():
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('--article_list_file', type=str, required=True)
    parser.add_argument('--max_articles', type=int)
    parser.add_argument('--articles_per_job', type=int)
    parser.add_argument('--wikidata_endpoint')
    # TODO: add max_jobs
    args = parser.parse_args()

    with open(args.article_list_file) as f:
        article_names = list(map(lambda line: line.strip(), list(f)))

    if args.max_articles:
        article_names = article_names[:args.max_articles]

    if not args.articles_per_job:
        slices = [article_names]
    else:
        slices = []
        for i in range(0, len(article_names), args.articles_per_job):
            slices.append(article_names[i:i+args.articles_per_job])

    for articles_slice in slices:
        launch_job_for_slice(articles_slice, args.wikidata_endpoint)

if __name__ == '__main__':
    main()
