"""
Tool for building labeled gold set from predictions of unknown truth value.
"""

from src.prototype.lib import flags
from src.prototype.eval import prediction

import os.path
import random

def main():
    flags.add_argument('--prediction_tsv', required=True)
    flags.add_argument('--gold_tsv', required=True)
    flags.make_parser(description='TODO')
    args = flags.parse_args()

    predictions = prediction.load_predictions(args.prediction_tsv)

    have_gold = set()
    gold_predictions = []
    if os.path.isfile(args.gold_tsv):
        gold_predictions = prediction.load_predictions(args.gold_tsv)
        for p in gold_predictions:
            have_gold.add((p.subject, p.relation, p.object))

    with open(args.gold_tsv, 'a') as f:
        for p in sorted(predictions, key=lambda p: p.score, reverse=True):
            if (p.subject, p.relation, p.object) in have_gold:
                continue
            if p.truth == '?':
                gold_predictions.append(p)

    prediction.write_predictions(gold_predictions, args.gold_tsv)
if __name__ == '__main__':
    main()
