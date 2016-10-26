from src.prototype.lib import flags
from src.prototype.eval import prediction
from src.prototype.lib import wikidata

import itertools
import progressbar

def add_labels_to_predictions(predictions, wikidata_client):
    print('Collecting entities to label...')
    bar = progressbar.ProgressBar(redirect_stdout=True)
    to_label = set(itertools.chain.from_iterable(
        (p.subject, p.relation, p.object) for p in bar(predictions)
    ))
    print('Adding labels...')
    labels = wikidata_client.get_names(to_label)

    def get_name(entity):
        if entity in labels:
            return labels[entity]
        else:
            return (wikidata_client.get_name(entity) or '??')

    for p in predictions:
        p.subject_label = get_name(p.subject)
        p.relation_label = get_name(p.relation)
        p.object_label = get_name(p.object)

def add_ground_truth_to_predictions(predictions, wikidata_client):
    subjects = {p.subject for p in predictions}
    relations = {p.relation for p in predictions}
    print('Looking for counterexamples...')
    subject_relation_pairs = set(wikidata_client.get_subject_relation_pairs(
        subjects,
        relations
    ))

    triples = [(p.subject, p.relation, p.object) for p in predictions]
    print('Validating predictions...')
    true_triples = wikidata_client.get_true_subset(triples)

    bar = progressbar.ProgressBar(redirect_stdout=True)
    for p in bar(predictions):
        if ((p.subject, p.relation, p.object) in true_triples):
            # truth
            truth = True
        elif (p.subject, p.relation) in subject_relation_pairs:
            # subject has that relation with something else; false
            truth = False
        else:
            truth = '?'
        p.truth = truth

def main():
    flags.add_argument('--prediction_tsv', required=True)
    flags.make_parser(description='TODO')
    args = flags.parse_args()

    wikidata_client = wikidata.WikidataClient()

    predictions = prediction.load_predictions(args.prediction_tsv)
    add_labels_to_predictions(predictions, wikidata_client)
    add_ground_truth_to_predictions(predictions, wikidata_client)
    print('Writing predictions')
    prediction.write_predictions(predictions, args.prediction_tsv)

if __name__ == '__main__':
    main()
