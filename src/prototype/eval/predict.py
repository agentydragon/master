import progressbar
from src.prototype.extraction import model as model_lib
from src.prototype.fusion import fuser as fuser_lib
from src.prototype.lib import flags
from src.prototype.lib import sample_repo
from src.prototype.lib import relations

from src.prototype.eval import prediction

def main():
    flags.add_argument('--output_tsv', required=True)
    flags.add_argument('--score_cutoff')
    flags.add_argument('--relation', action='append')
    flags.make_parser(description='TODO')
    args = flags.parse_args()

    predictions = []

    if args.relation:
        rs = args.relation
    else:
        rs = relations.RELATIONS

    for i, relation in enumerate(rs):
        print('Relation', relation)

        print('Loading samples for relation', relation)
        all_samples = sample_repo.load_samples(relation, 'test-known') # + sample_repo.load_samples(relation, 'test-unknown')

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

        print("Predicting...")
        scores = model.predict_proba(all_samples)

        print("Fusing...")
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
