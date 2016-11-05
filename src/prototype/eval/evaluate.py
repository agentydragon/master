from src.prototype.lib import flags
from src.prototype.eval import prediction

import random

def select_predictions(predictions, min_score=None, max_score=None):
    return [p for p in predictions
            if (((min_score is None) or p.score >= min_score) and
                ((max_score is None) or p.score <= max_score))]

def show_calibration(predictions):
    positives = [p for p in predictions if p.truth == True]
    negatives = [p for p in predictions if p.truth == False]
    unknowns = [p for p in predictions if p.truth == '?']

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

        scores = [p.score for p in pos_samples + neg_samples]
        avg_score = sum(scores) / len(scores)

        print('%.2f positive %.2f negative:' % (threshold, (1.0 - threshold)),
              'average score %.4f' % avg_score)

    print()

    def show_threshold_calibration(thresholds):
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
                print('[%.2f;%.2f]: %.2f%% true (%d true %d false)' %
                      (min_score, max_score, 100 * float(true) / (true + false),
                       true, false))

    show_threshold_calibration([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    show_threshold_calibration([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])

    # TODO: What's the average truth-ness of prediction with scores [0.2;0.3)?

def show_counts(predictions):
    for threshold in [0.1, 0.5, 0.9, 0.95, 0.99]:
        predicted = len(select_predictions(predictions, min_score=threshold))
        print('Number of predictions above', threshold, ':', predicted)

def main():
    flags.add_argument('--prediction_tsv', required=True)
    flags.add_argument('--show_above_threshold', type=float)
    flags.add_argument('--show_calibration', type=bool)
    flags.add_argument('--show_counts', type=bool)
    flags.make_parser(description='TODO')
    args = flags.parse_args()

    predictions = prediction.load_predictions(args.prediction_tsv)

    if args.show_above_threshold:
        print('Predictions above %.4f:' % args.show_above_threshold)
        for p in select_predictions(predictions,
                                    min_score=args.show_above_threshold):
            print('\t'.join([
                p.subject_label,
                p.relation_label,
                p.object_label,
                '%.4f' % (p.score),
                str(p.truth),
            ]))
        print()

    if args.show_calibration:
        show_calibration(predictions)

    if args.show_counts:
        show_counts(predictions)

if __name__ == '__main__':
    main()
