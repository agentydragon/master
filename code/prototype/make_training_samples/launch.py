#!/usr/bin/python3

from prototype.lib import mapper
from prototype.lib import article_set
from prototype.lib import zk
import argparse

zk.start()

def main():
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('--article_list_file', default=None)
    parser.add_argument('--max_articles', type=int, default=None)
    parser.add_argument('--articles_per_job', type=int)
    parser.add_argument('--wikidata_endpoint')
    parser.add_argument('--dbpedia_endpoint')
    parser.add_argument('--local_parallelism', type=int, default=1)
    # TODO: add max_jobs
    args = parser.parse_args()

    def make_commandline(articles_slice):
        wikidata = args.wikidata_endpoint
        if not wikidata:
            zk_wikidata = zk.get_wikidata_endpoint()
            if zk_wikidata:
                wikidata = ('http://%s/wikidata/query' % zk_wikidata)
            else:
                wikidata = ''

        dbpedia = args.dbpedia_endpoint
        if not dbpedia:
            zk_dbpedia = zk.get_dbpedia_endpoint()
            if zk_dbpedia:
                dbpedia = ('http://%s/dbpedia-sameas/query' % zk_dbpedia)
            else:
                dbpedia = ''

        job_command = [
            'prototype/make_training_samples/make_training_samples',
            '--parallelism', str(args.local_parallelism),
            '--wikidata_endpoint', wikidata,
            '--dbpedia_endpoint', dbpedia,
        ]
        for article in articles_slice:
            job_command.extend(['--articles', article])
        print(job_command)
        return job_command

    def slice_to_walltime(articles_slice):
        article_count = len(articles_slice)
        walltime_estimate = round(
            (120 * article_count / float(args.local_parallelism)) * 2 + 100
        ) # or default: "04:00:00"
        return walltime_estimate

    art_set = article_set.ArticleSet(
        path = args.article_list_file,
        maximum = args.max_articles
    )

    mapper.launch_in_slices(
        'make-training-samples',
        art_set.article_names,
        args.articles_per_job,
        make_commandline,
        slice_to_walltime,
        cores=max(2, args.local_parallelism)
    )

if __name__ == '__main__':
    main()
