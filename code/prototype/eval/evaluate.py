from prototype.lib import flags

import random
import recordclass
import progressbar

Prediction = recordclass.recordclass(
    "Prediction",
    ["score", "subject", "relation", "object",
     "subject_label", "relation_label", "object_label",
     "truth"]
)

def select_predictions(predictions, min_score=None, max_score=None):
    return [p for p in predictions
            if (((min_score is None) or p.score >= min_score) and
                ((max_score is None) or p.score <= max_score))]

def show_calibration(predictions):
    positives = [prediction for prediction in predictions if prediction.truth == True]
    negatives = [prediction for prediction in predictions if prediction.truth == False]
    unknowns = [prediction for prediction in predictions if prediction.truth == '?']

    print('%d positives, %d negatives, %d unknowns' %
          (len(positives), len(negatives), len(unknowns)))

    for threshold in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
        count = 200
        select_positives = round(count * threshold)
        if len(positives) < select_positives:
            print(threshold, 'avg score undefined (not enough positives)')
            continue
        pos_samples = random.sample(positives, select_positives)
        select_negatives = round(count * (1.0 - threshold))
        if len(negatives) < select_negatives:
            print(threshold, 'avg score undefined (not enough negatives)')
            continue
        neg_samples = random.sample(negatives, select_negatives)

        scores = [prediction.score for prediction in pos_samples + neg_samples]
        avg_score = sum(scores) / len(scores)

        print('%.2f positive %.2f negative:' % (threshold, (1.0 - threshold)),
              'average score %.4f' % avg_score)

    print()

    thresholds = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    for i in range(len(thresholds) - 1):
        min_score, max_score = thresholds[i], thresholds[i + 1]
        predicts = select_predictions(predictions,
                                      min_score = min_score,
                                      max_score = max_score)
        true = len([p for p in predicts if p.truth == True])
        false = len([p for p in predicts if p.truth == False])
        if true + false == 0:
            print('[%.2f;%.2f]: no predictions in this range' %
                  (min_score, max_score))
        else:
            print('[%.2f;%.2f]: %.2f%% true' %
                  (min_score, max_score, 100 * float(true) / (true + false)))

    # TODO: What's the average truth-ness of prediction with scores [0.2;0.3)?

def show_counts(predictions):
    for threshold in [0.1, 0.5, 0.9, 0.95, 0.99]:
        predicted = len(select_predictions(predictions, min_score=threshold))
        print('Number of predictions above', threshold, ':', predicted)

def main():
    flags.add_argument('--article', action='append')
    flags.add_argument('--prediction_tsv', required=True)
    flags.add_argument('--show_all_predictions', type=bool)
    flags.add_argument('--show_calibration', type=bool)
    flags.add_argument('--show_counts', type=bool)
    flags.make_parser(description='TODO')
    args = flags.parse_args()

    with open(args.prediction_tsv, 'r') as f:
        predictions = []
        for line in f:
            score, subject, relation, object, subject_label, relation_label, object_label, truth = line.strip().split('\t')

            if truth == '+':
                truth = True
            elif truth == '-':
                truth = False
            elif truth == '?':
                truth = '?'
            else:
                raise

            prediction = Prediction(
                score = float(score),
                subject = subject,
                relation = relation,
                object = object,
                subject_label = subject_label,
                relation_label = relation_label,
                object_label = object_label,
                truth = truth
            )
            predictions.append(prediction)

        if args.show_all_predictions:
            for prediction in predictions:
                print(prediction.subject_label, prediction.relation_label,
                      prediction.object_label, prediction.score,
                      prediction.truth)

        if args.show_calibration:
            show_calibration(predictions)

        if args.show_counts:
            show_counts(predictions)

if __name__ == '__main__':
    main()
