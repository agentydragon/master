from prototype.lib import sample_repo
from prototype.make_training_samples import sample_generation
from py import wikidata
import argparse

def main():
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('--article_list_file', required=True)
    parser.add_argument('--wikidata_endpoint')
    parser.add_argument('--count_per_relation', default=10, type=int)
    args = parser.parse_args()

    wikidata_client = wikidata.WikidataClient(args.wikidata_endpoint or None)

    with open(args.article_list_file) as f:
        article_names = list(map(lambda line: line.strip(), list(f)))

    for relation in sample_repo.all_relations():
        samples = []
        for i in range(args.count_per_relation):
            sample = sample_generation.sample_negative(article_names,
                                                        relation,
                                                        wikidata_client).to_json()
            samples.append(sample)
        sample_repo.write_negative_samples(relation, samples)
        print("Produced negatives for", relation)

if __name__ == '__main__':
    main()
