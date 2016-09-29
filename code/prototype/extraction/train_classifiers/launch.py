from prototype.lib import sample_repo
from prototype.lib import relations
from prototype.lib import mapper
from prototype.lib import flags

def main():
    flags.add_argument('--relations_per_job', type=int)
    flags.make_parser(description='TODO')
    args = flags.parse_args()

    CORES = 16

    def make_commandline(relations_slice):
        job_command = [
            '../cpulimit/cpulimit',
            '--limit=' + str(CORES * 100),
            '--include-children',
            'prototype/train_classifiers/train_classifiers',
        ]
        for relation in relations_slice:
            job_command.extend(['--relation', relation])
        return job_command

    def slice_to_walltime(relations_slice):
        # TODO: more precise
        # 1 hour is not enough to train 4 classifiers
        return "04:00:00"

    mapper.launch_in_slices(
        'train-classifiers',
        relations.RELATIONS,
        args.relations_per_job,
        make_commandline,
        slice_to_walltime,
        cores=CORES,
        ram='8gb'
    )

if __name__ == '__main__':
    main()
