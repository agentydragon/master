import progressbar
from prototype.extraction import model as model_lib
from prototype.extraction import feature_extraction
from prototype.fusion import fuser as fuser_lib
# from prototype.lib import file_util
from prototype.lib import flags
from prototype.lib import article_set
from prototype.lib import sample_repo
from prototype.lib import sample_generation
from prototype.lib import relations
from prototype.lib import wikidata
# import paths

import recordclass

Prediction = recordclass.recordclass(
    "Prediction",
    ["score", "subject", "relation", "object",
     "subject_label", "relation_label", "object_label",
     "truth"]
)

def add_labels_to_predictions(predictions, wikidata_client):
    print('Adding labels...')
    to_label = set()
    for prediction in predictions:
        to_label = to_label.union({
            prediction.subject,
            prediction.relation,
            prediction.object
        })
    labels = wikidata_client.get_names(to_label)

    def get_name(entity):
        if entity in labels:
            return labels[entity]
        else:
            return wikidata_client.get_name(entity)

    for prediction in predictions:
        prediction.subject_label = get_name(prediction.subject)
        prediction.relation_label = get_name(prediction.relation)
        prediction.object_label = get_name(prediction.object)

def add_ground_truth_to_predictions(predictions, wikidata_client):
    subjects = {prediction.subject for prediction in predictions}
    relations = {prediction.relation for prediction in predictions}
    print('Looking for counterexamples...')
    subject_relation_pairs = wikidata_client.get_subject_relation_pairs(
        subjects,
        relations
    )

    triples = [(p.subject, p.relation, p.object) for p in predictions]
    print('Validating predictions...')
    true_triples = wikidata_client.get_true_subset(triples)

    for prediction in predictions:
        if ((prediction.subject, prediction.relation, prediction.object)
                in true_triples):
            # truth
            truth = True
        elif (prediction.subject, prediction.relation) in subject_relation_pairs:
            # subject has that relation with something else; false
            truth = False
        else:
            truth = '?'
        prediction.truth = truth

def write_predictions(predictions, tsv_path):
    with open(tsv_path, 'w') as f:
        for prediction in predictions:
            if prediction.truth == True:
                truth = '+'
            elif prediction.truth == False:
                truth = '-'
            elif prediction.truth == '?':
                truth = '?'
            else:
                raise

            f.write('\t'.join([
                "%.4f" % prediction.score,
                prediction.subject,
                prediction.relation,
                prediction.object,
                prediction.subject_label,
                prediction.relation_label,
                prediction.object_label,
                truth
            ]))

def load_samples(articles):
    all_samples = []
    bar = progressbar.ProgressBar(redirect_stdout=True)
    # articles = articles[:10]
    for title in bar(articles):
        document = sample_generation.try_load_document(title)
        if not document:
            # print('Cannot load document', title, ':(')
            continue
        document_samples = sample_generation.get_all_document_samples(
            document = document
        )
        all_samples.extend(document_samples)
    return all_samples

def main():
    flags.add_argument('--article', action='append')
    flags.add_argument('--output_tsv', required=True)
    flags.add_argument('--score_cutoff')
    flags.make_parser(description='TODO')
    args = flags.parse_args()

    wikidata_client = wikidata.WikidataClient()

    if args.article:
        articles = args.article
    else:
        # TODO: make some sense of the sets
        art_set = article_set.ArticleSet()
        train, test, calibrate = art_set.split_train_test_calibrate()
        # articles = test
        articles = calibrate

    all_samples = load_samples(articles)
    predictions = []

    for relation in relations.RELATIONS:
        print("Loading model for %s." % relation)
        try:
            model = model_lib.Model.load(relation)
        except Exception as e:
            print('Failed to load model for', relation, ':(')
            print(e)
            print('Skipping relation, cannot load model')
            continue

        scores = model.predict_proba(all_samples)

        by_entities = {}
        for i, sample in enumerate(all_samples):
            key = (sample.subject, sample.object)
            if key not in by_entities:
                by_entities[key] = []
            # TODO: Fix this: why [1]?
            by_entities[key].append(scores[i][1])

        fuser = fuser_lib.Fuser.load(relation)
        bar = progressbar.ProgressBar(redirect_stdout=True)
        for subject, object in bar(by_entities):
            score = fuser.predict_proba(by_entities[(subject, object)])

            if args.score_cutoff and score < args.score_cutoff:
                continue

            predictions.append(Prediction(
                score = score,
                subject = subject,
                relation = relation,
                object = object,
                subject_label = None,
                relation_label = None,
                object_label = None,
                truth = None
            ))

    add_labels_to_predictions(predictions, wikidata_client)
    add_ground_truth_to_predictions(predictions, wikidata_client)
    write_predictions(predictions, args.output_tsv)

if __name__ == '__main__':
    main()
