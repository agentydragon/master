from prototype.lib import sample_repo
from prototype.lib import sample_generation
from prototype.lib import wikidata
from prototype.lib import flags
# import progressbar

def process_article(article_title):
    wikidata_client = wikidata.WikidataClient()

    samples = sample_generation.get_samples_from_document(
        article_title,
        wikidata_client = wikidata_client
    )
    if not samples:
        return
    try:
        sample_repo.write_article(article_title, samples)
    except sample_repo.SavingError as e:
        print("Error during processing article '%s'" % article_title)
        print(e)
    except e:
        print("Error during processing article '%s'" % article_title)
        print(e)
        raise
    return

def main():
    flags.add_argument('--articles', action='append')
    flags.make_parser(description='TODO')
    args = flags.parse_args()

    # bar = progressbar.ProgressBar(redirect_stdout=True)
    # for article in bar(args.articles):
    for article in args.articles:
        print(article)
        process_article(article)

if __name__ == '__main__':
    main()
