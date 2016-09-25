from prototype.lib import sample_repo
from prototype.lib import mapper
from prototype.lib import flags
from prototype.lib import wikidata

def main():
    flags.add_argument('--relations_per_job', type=int)
    flags.add_argument('--article_list_file', required=True)
    flags.add_argument('--count_per_relation', type=int, default=1000)
    flags.add_argument('--local_parallelism', type=int, default=4)
    flags.make_parser(description='TODO')
    args = flags.parse_args()

    def make_commandline(relations_slice):
        job_command = [
            'prototype/add_negative_samples/add_negative_samples',
            '--article_list_file', args.article_list_file,
            '--count_per_relation', str(args.count_per_relation),
            '--parallelism', str(args.local_parallelism),
            '--wikidata_endpoint', wikidata.get_default_endpoint_url(),
        ]
        for relation in relations_slice:
            job_command.extend(['--relation', relation])
        return job_command

    def slice_to_walltime(relations_slice):
        seconds_per_sample = 1
        total_time = len(relations_slice) * args.count_per_relation * seconds_per_sample
        return round(total_time / float(args.local_parallelism))

    mapper.launch_in_slices('add-negative-samples',
                            sample_repo.all_relations(),
                            args.relations_per_job,
                            make_commandline,
                            slice_to_walltime,
                            cores=max(2, args.local_parallelism),
                            ram='8gb')

if __name__ == '__main__':
    main()
