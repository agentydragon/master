#!/usr/bin/python3

from py import pbs_util
from py import paths
from py import file_util
from prototype.lib import sample_repo
import argparse
import subprocess
import datetime

now = datetime.datetime.now()

def launch_job_for_slice(i, article_list_file, relations_slice, wikidata_endpoint): #, parallelism):
    job_name = 'add-negative-samples'

    log_base_dir = paths.LOG_PATH + "/" + job_name + "/" + now.strftime('%Y%m%d-%H%M%S')
    file_util.ensure_dir(log_base_dir)

    job_command = ['prototype/add_negative_samples/add_negative_samples'
                   '--article_list_file', article_list_file,
                   ]
    if wikidata_endpoint:
        job_command.extend(['--wikidata_endpoint', wikidata_endpoint])
    for relation in relations_slice:
        job_command.extend(['--relation', relation])
    job_command.extend(['--count_per_relation', '1000'])

    # TODO
    walltime_estimate = "04:00:00"

    job = pbs_util.launch_job(
        # TODO: parallelize on one node
        walltime=walltime_estimate,
        node_spec="nodes=1:brno:ppn=2,mem=2gb",
        job_name=job_name,
        job_command=job_command,
        output_path=(log_base_dir + ("/%04d.o" % i)),
        error_path=(log_base_dir + ("/%04d.e" % i))
    )
    print("Launched %s:" % job_name, job.job_id)

def main():
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('--relations_per_job', type=int)
    parser.add_argument('--wikidata_endpoint')
    parser.add_argument('--article_list_file', required=True)
    args = parser.parse_args()

    relations = sample_repo.all_relations()

    if not args.relations_per_job:
        slices = [relations]
    else:
        slices = []
        for i in range(0, len(relations), args.relations_per_job):
            slices.append(relations[i:i+args.relations_per_job])

    for i, relation_slice in enumerate(slices):
        launch_job_for_slice(i, args.article_list_file, relation_slice, args.wikidata_endpoint)

if __name__ == '__main__':
    main()
