import json
import progressbar
from prototype import feature_extraction
from prototype.lib import flags
from prototype.lib import article_set
from prototype.lib import sample_generation
from prototype.lib import wikidata
from prototype.lib import relations
from scipy import sparse
from sklearn import linear_model
from sklearn import metrics
from sklearn import cross_validation
import math
import numpy
import paths
import pickle

# load classifiers

flags.add_argument('--json_in', required=True)
flags.make_parser(description='TODO')
args = flags.parse_args()

with open(args.json_in, 'r') as f:
    by_relation = json.load(f)

def sentence_scores_to_features(sentence_scores):
    return [
        math.log(len(sentence_scores)),
        math.sqrt(len(sentence_scores)),
        sum(sentence_scores) / len(sentence_scores),
    ]

def train_relation_fuser(relation, samples):
    positive_sentence_scores = samples['true']
    negative_sentence_scores = samples['false']

    features = []
    labels = []

    for sample in positive_sentence_scores:
        features.append(sentence_scores_to_features(sample))
        labels.append(1)

    for sample in negative_sentence_scores:
        features.append(sentence_scores_to_features(sample))
        labels.append(0)

    # train-test split
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(
        features, labels, test_size=0.33, random_state=42)

    # TODO: Decision trees instead?
    clf = linear_model.LogisticRegression(verbose=True)
    clf.fit(X_train, y_train)
    score = clf.decision_function(X_test)

    fpr, tpr, _ = metrics.roc_curve(y_test, score)
    auc = metrics.auc(fpr, tpr)
    print("%s AUC:" % relation, auc)

    predicted = clf.predict(X_test)
    print("%s accuracy:" % relation, numpy.mean(predicted == y_test))

    feature_extraction.plot_roc_general(
        fpr,
        tpr,
        '%s (area = %.02f)' % (relation, auc),
        paths.CHARTS_PATH + '/' + relation + '.png'
    )

for relation in relations.RELATIONS:
    samples = by_relation[relation]
    train_relation_fuser(relation, samples)
