from prototype.lib import sample_repo
from prototype.lib import relations
from prototype.lib import mapper
from prototype.lib import flags
from prototype.lib import wikidata

def main():
    flags.add_argument('--relations_per_job', type=int)
    flags.make_parser(description='TODO')
    args = flags.parse_args()

    def make_commandline(relations_slice):
        job_command = [
            'prototype/extraction/train_classifiers/train_classifiers',
            '--wikidata_endpoint', wikidata.get_default_endpoint_url(),
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
        cores=16,
        ram='8gb'
    )

if __name__ == '__main__':
    main()
