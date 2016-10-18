import progressbar
import itertools
from prototype.extraction import model as model_lib
from prototype.extraction import feature_extraction
from prototype.fusion import fuser as fuser_lib
# from prototype.lib import file_util
from prototype.lib import flags
from prototype.lib import article_set
from prototype.lib import sample_repo
from prototype.lib import sample_generation
from prototype.lib import relations
# import paths

from prototype.eval import prediction

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
    flags.add_argument('--n_articles', type=int)
    flags.make_parser(description='TODO')
    args = flags.parse_args()

    if args.article:
        articles = args.article
    else:
        # TODO: make some sense of the sets
        art_set = article_set.ArticleSet()
        train, test, calibrate = art_set.split_train_test_calibrate()
        articles = test
        # articles = calibrate

    if args.n_articles:
        articles = articles[:args.n_articles]

    all_samples = load_samples(articles)
    predictions = []

    for i, relation in enumerate(relations.RELATIONS):
        print("Loading model for %s (%d of %d)." % (
            relation, (i + 1), len(relations.RELATIONS)
        ))
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

            if args.score_cutoff and score < float(args.score_cutoff):
                continue

            predictions.append(prediction.Prediction(
                score = score,
                subject = subject,
                relation = relation,
                object = object,
                subject_label = None,
                relation_label = None,
                object_label = None,
                truth = '?'
            ))

    prediction.write_predictions(predictions, args.output_tsv)

if __name__ == '__main__':
    main()
