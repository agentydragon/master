from prototype.lib import sample_repo
from prototype.make_training_samples import sample_generation
from py import wikidata
import argparse
import multiprocessing

def generate_negatives_for_relation(article_names, relation, count, wikidata_client):
    def make_sample(i):
        print(i)
        return sample_generation.sample_negative(article_names,
                                                 relation,
                                                 wikidata_client).to_json()
    samples = map(make_sample, range(count))
    sample_repo.write_negative_samples(relation, list(samples))
    print("Produced negatives for", relation)

def main():
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('--article_list_file', required=True)
    parser.add_argument('--wikidata_endpoint')
    parser.add_argument('--count_per_relation', default=10, type=int)
    parser.add_argument('--relation')
    args = parser.parse_args()

    wikidata_client = wikidata.WikidataClient(args.wikidata_endpoint or None)

    with open(args.article_list_file) as f:
        article_names = list(map(lambda line: line.strip(), list(f)))

    if not args.relation:
        for relation in sample_repo.all_relations():
            generate_negatives_for_relation(article_names, relation,
                                            args.count_per_relation,
                                            wikidata_client)
    else:
        generate_negatives_for_relation(article_names, args.relation,
                                        args.count_per_relation,
                                        wikidata_client)

if __name__ == '__main__':
    main()
