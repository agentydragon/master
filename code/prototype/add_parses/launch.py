from prototype.lib import flags
from prototype.lib import mapper
from prototype.lib import article_set

def main():
    flags.add_argument('--articles_per_job', type=int)
    flags.make_parser(description='TODO')
    # TODO: add max_jobs
    args = flags.parse_args()

    art_set = article_set.ArticleSet()

    def make_commandline(articles_slice)
        return ['prototype/add_parses/add_parses'] + articles_slice

    mapper.launch_in_slices(
        'add-parses',
        article_names,
        args.articles_per_job,
        make_commandline,
        slice_to_walltime=(lambda s: return "01:00:00"),
        cores=4,
        ram='9gb'
    )

if __name__ == '__main__':
    main()
