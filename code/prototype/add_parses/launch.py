istmport argparse
from prototype.lib import mapper

def main():
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('--article_list_file',
                        default=paths.ARTICLE_LIST_PATH)
    parser.add_argument('--max_articles', type=int)
    parser.add_argument('--articles_per_job', type=int)
    # TODO: add max_jobs
    args = parser.parse_args()

    with open(args.article_list_file) as f:
        article_names = list(map(lambda line: line.strip(), list(f)))

    if args.max_articles:
        article_names = article_names[:args.max_articles]

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
