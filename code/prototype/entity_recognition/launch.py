from prototype.lib import flags
from prototype.lib import article_set
from prototype.lib import mapper

def main():
    flags.add_argument('--force_redo')
    flags.add_argument('--articles_per_job', type=int, required=True)
    flags.make_parser(description='TODO')
    args = flags.parse_args()

    art_set = article_set.ArticleSet()

    def make_commandline(articles_slice):
        job_command = [
            'prototype/entity_recognition/entity_recognition',
        ]

        if args.force_redo:
            job_command.extend(['--force_redo=true'])

        for name in articles_slice:
            job_command.extend(['--articles', name])

        return job_command

    # (2016-10-10 prvak) 4 cores crash on startup sometimes (not sure how, cpulimit should prevent that)
    mapper.launch_in_slices(
        'add-spotlight',
        art_set.article_names,
        args.articles_per_job,
        make_commandline,
        slice_to_walltime=(lambda s: "02:00:00"),
        # cores=1,
        cores=8,
        # ram='1gb'
        ram='16gb'
        # TODO: scratch
    )

if __name__ == '__main__':
    main()
