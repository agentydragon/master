from prototype.lib import sample_repo
from prototype.lib import sample_generation
from prototype.lib import wikidata
import argparse
import multiprocessing

def process_article(article_title):
    global wikidata_endpoint
    wikidata_client = wikidata.WikidataClient(wikidata_endpoint or None)

    samples = sample_generation.get_samples_from_document(
        article_title,
        wikidata_client=wikidata_client
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
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('--articles', action='append')
    parser.add_argument('--wikidata_endpoint')
                        # description='example: https://query.wikidata.org/sparql, or http://hador:3030/wikidata/query')
    parser.add_argument('--parallelism', default=1, type=int)
    args = parser.parse_args()

    global wikidata_endpoint
    wikidata_endpoint = args.wikidata_endpoint

    assert args.parallelism >= 1
    if args.parallelism == 1:
        for article in args.articles:
            process_article(article)
    else:
        pool = multiprocessing.Pool(args.parallelism)
        pool.map(process_article, args.articles)

if __name__ == '__main__':
    main()
