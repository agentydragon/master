from prototype.lib import sample_repo
from prototype.lib import mapper
from prototype.lib import flags

def main():
    flags.add_argument('--relations_per_job', type=int)
    flags.add_argument('--local_parallelism', type=int, default=4)
    flags.make_parser(description='TODO')
    args = flags.parse_args()

    def make_commandline(relations_slice):
        job_command = [
            'prototype/train_classifiers/train_classifiers',
            '--parallelism', str(args.local_parallelism)
        ]
        for relation in relations_slice:
            job_command.extend(['--relation', relation])
        return job_command

    def slice_to_walltime(relations_slice):
        # TODO: more precise
        # 1 hour is not enough to train 4 classifiers
        return "04:00:00"

    mapper.launch_in_slices('train-classifiers',
                            sample_repo.all_relations(),
                            args.relations_per_job,
                            make_commandline,
                            slice_to_walltime,
                            cores=max(2, args.local_parallelism),
                            ram='8gb')

if __name__ == '__main__':
    main()
