import recordclass

Prediction = recordclass.recordclass(
    "Prediction",
    ["score", "subject", "relation", "object",
     "subject_label", "relation_label", "object_label",
     "truth"]
)

def load_predictions(tsv_path):
    with open(tsv_path, 'r') as f:
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
    return predictions

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
                (prediction.subject_label or '??'),
                (prediction.relation_label or '??'),
                (prediction.object_label or '??'),
                truth
            ]) + '\n')
