from prototype.lib import flags
from prototype.lib import article_set
from prototype.lib import mapper

def main():
    # TODO: add max_jobs
    flags.add_argument('--articles_per_job', type=int)
    flags.make_parser(description='TODO')
    args = flags.parse_args()

    art_set = article_set.ArticleSet()

    def make_commandline(articles_slice):
        job_command = [
            'prototype/add_join/add_join',
        ]

        for name in articles_slice:
            job_command.extend(['--articles', name])

        return job_command

    mapper.launch_in_slices('add-join',
                            article_names,
                            args.articles_per_job,
                            make_commandline,
                            slice_to_walltime=(lambda s: return "01:00:00"),
                            cores=1,
                            ram='1gb')

if __name__ == '__main__':
    main()
