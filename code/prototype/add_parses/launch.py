import argparse
from prototype.lib import mapper
from prototype.lib import article_set

def main():
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('--article_list_file', default=None)
    parser.add_argument('--max_articles', type=int, default=None)
    parser.add_argument('--articles_per_job', type=int)
    # TODO: add max_jobs
    args = parser.parse_args()

    art_set = article_set.ArticleSet(
        path = args.article_list_file,
        maximum = args.max_articles
    )

    def make_commandline(articles_slice)
        return ['prototype/add_parses/add_parses'] + articles_slice

    mapper.launch_in_slices('add-parses',
                            article_names,
                            args.articles_per_job,
                            make_commandline,
                            slice_to_walltime=(lambda s: return "01:00:00"),
                            cores=4,
                            ram='9gb')

if __name__ == '__main__':
    main()
