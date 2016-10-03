from prototype.lib import flags
from prototype.lib import article_set
from prototype.lib import mapper
from prototype.entity_recognition import spotlight

def main():
    flags.add_argument('--force_redo')
    flags.add_argument('--articles_per_job', type=int, required=True)
    flags.make_parser(description='TODO')
    args = flags.parse_args()

    art_set = article_set.ArticleSet()

    spotlight_endpoint = spotlight.get_default_spotlight_endpoint()

    def make_commandline(articles_slice):
        job_command = [
            'prototype/entity_recognition/entity_recognition',
            '--spotlight_endpoint', spotlight_endpoint,
        ]

        if args.force_redo:
            job_command.extend(['--force_redo=true'])

        for name in articles_slice:
            job_command.extend(['--articles', name])

        return job_command

    mapper.launch_in_slices(
        'add-spotlight',
        art_set.article_names,
        args.articles_per_job,
        make_commandline,
        slice_to_walltime=(lambda s: "01:00:00"),
        cores=1,
        ram='1gb'
    )

if __name__ == '__main__':
    main()
