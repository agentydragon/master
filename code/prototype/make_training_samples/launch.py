#!/usr/bin/python3

from py import pbs_util
from py import paths
from py import file_util
import argparse
import subprocess
import datetime

now = datetime.datetime.now()
log_base_dir = paths.LOG_PATH + "/make-training-samples/" + now.strftime('%Y%m%d-%H%M%S')
file_util.ensure_dir(log_base_dir)

def launch_job_for_slice(i, articles_slice, wikidata_endpoint, parallelism):
    job_command = ['prototype/make_training_samples/make_training_samples',
                   '--parallelism', str(parallelism)]
    if wikidata_endpoint:
        job_command.extend(['--wikidata_endpoint', wikidata_endpoint])
    for article in articles_slice:
        job_command.extend(['--articles', article])

    # 15 minutes per 100-article job -> 9 seconds/article
    # pessimistic: twice as much, 100 seconds for startup

    walltime_estimate = str(round((9 * len(articles_slice) / float(parallelism)) * 2 + 100))  # or default: "04:00:00"

    job = pbs_util.launch_job(
        # TODO: parallelize on one node
        walltime=walltime_estimate,
        node_spec="nodes=1:brno:ppn=" + str(max(2, parallelism)) + ",mem=2gb",
        job_name="make-training-samples",
        job_command=job_command,
        output_path=(log_base_dir + ("/%04d.o" % i)),
        error_path=(log_base_dir + ("/%04d.e" % i))
    )
    print("Launched make-training-samples:", job.job_id)

def main():
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('--article_list_file', type=str, required=True)
    parser.add_argument('--max_articles', type=int)
    parser.add_argument('--articles_per_job', type=int)
    parser.add_argument('--wikidata_endpoint')
    parser.add_argument('--local_parallelism', type=int, default=1)
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

    for i, articles_slice in enumerate(slices):
        launch_job_for_slice(i, articles_slice, args.wikidata_endpoint,
                             parallelism=args.local_parallelism)

if __name__ == '__main__':
    main()
