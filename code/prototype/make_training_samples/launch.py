#!/usr/bin/python3

from prototype.lib import mapper
import paths
import argparse

def main():
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('--article_list_file',
                        default=paths.ARTICLE_LIST_PATH)
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

    def make_commandline(articles_slice):
        job_command = [
            'prototype/make_training_samples/make_training_samples',
            '--parallelism', str(args.local_parallelism)
        ]
        if args.wikidata_endpoint:
            job_command.extend(['--wikidata_endpoint', args.wikidata_endpoint])
        for article in articles_slice:
            job_command.extend(['--articles', article])
        return job_command

    def slice_to_walltime(articles_slice):
        article_count = len(articles_slice)
        walltime_estimate = round(
            (60 * article_count / float(args.local_parallelism)) * 2 + 100
        ) # or default: "04:00:00"
        return walltime_estimate

    mapper.launch_in_slices('make-training-samples',
                            article_names,
                            args.articles_per_job,
                            make_commandline,
                            slice_to_walltime,
                            cores=max(2, args.local_parallelism))

if __name__ == '__main__':
    main()
