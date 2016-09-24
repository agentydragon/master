import argparse
from prototype.lib import article_set
from prototype.lib import mapper

def main():
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('--article_list_file', default=None)
    parser.add_argument('--max_articles', type=int, default=None)
    parser.add_argument('--spotlight_endpoint')
    parser.add_argument('--force_redo')
    # TODO: add max_jobs
    parser.add_argument('--articles_per_job', type=int)
    args = parser.parse_args()

    art_set = article_set.ArticleSet(
        path = args.article_list_file,
        maxium = args.max_articles
    )

    def make_commandline(articles_slice):
        job_command = ['prototype/add_spotlight/add_spotlight']
        if args.spotlight_endpoint:
            job_command.extend(['--spotlight_endpoint',
                                args.spotlight_endpoint])
        if args.force_redo:
            job_command.extend(['--force_redo=true'])

        for name in articles_slice:
            job_command.extend(['--articles', name])

        return job_command

    mapper.launch_in_slices('add-spotlight',
                            article_names,
                            args.articles_per_job,
                            make_commandline,
                            slice_to_walltime=(lambda s: return "01:00:00"),
                            cores=1,
                            ram='1gb')

if __name__ == '__main__':
    main()
