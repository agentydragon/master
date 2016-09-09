from prototype.lib import sample_repo
from py import paths
from py import wikidata
import argparse

client = wikidata.WikidataClient()

def show_all_relations():
    for relation in sample_repo.all_relations():
        samples = sample_repo.load_samples(relation)
        print(relation, client.get_name(relation), ":", len(samples), "samples")

def main():
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('--relation')
    args = parser.parse_args()

    if args.relation:
        relation = args.relation

        samples = sample_repo.load_samples(relation)

        html = "<h1>" + relation + ": " + client.get_name(relation) + "</h1>"

        for sample in samples:
            html += "<li>" + sample.subject + " " + sample.object + " " + sample.sentence.text
            html += str(sample.to_json())

        print(html)
    else:
        show_all_relations()

if __name__ == '__main__':
    main()
