from prototype.lib import sample_repo
import paths
import argparse
from prototype.lib import wikidata
from prototype.lib import file_util
import numpy
from scipy import sparse
from sklearn import metrics
from sklearn import naive_bayes
from sklearn import cross_validation
from sklearn import linear_model
import pickle
from prototype import feature_extraction

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot

import multiprocessing

wikidata_client = wikidata.WikidataClient()

def train_classifier_for_relation(relation):
    relation_name = wikidata_client.get_name(relation)
    print('Training classifier for relation:',
          relation, relation_name)

    try:
        relation_samples = sample_repo.load_samples(relation)
    except AssertionError:
        return  # TODO HAX
    positive_count = len([sample for sample in relation_samples
                          if sample.positive])
    print('Positive:', positive_count)
    negative_count = len([sample for sample in relation_samples
                          if not sample.positive])
    print('Negative:', negative_count)

    if positive_count < 10 or negative_count < 10:
        print('Too few samples to train for', relation, '.')
        return

    things = list(map(feature_extraction.sample_to_features_label,
                      relation_samples)) # [:10]
    all_features = set()
    for thing in things:
        all_features = all_features.union(thing[0])
    all_features = list(sorted(all_features))

    matrix = sparse.lil_matrix((len(relation_samples), len(all_features)), dtype=numpy.int8)
    for i, thing in enumerate(things):
        for feature in thing[0]:
            matrix[i, all_features.index(feature)] = 1

    target = [thing[1] for thing in things]
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(
        matrix, target, test_size=0.33, random_state=42)

    def plot_roc(fpr, tpr, auc, prefix):
        pyplot.figure()
        pyplot.plot(fpr, tpr, label='ROC curve -- %s %s (area = %0.2f)' %
                    (relation, relation_name, auc))
        pyplot.plot([0, 1], [0, 1], 'k--')
        pyplot.xlim([0.0, 1.0])
        pyplot.ylim([0.0, 1.0])
        pyplot.xlabel('False Positive Rate')
        pyplot.ylabel('True Positive Rate')
        pyplot.legend(loc="lower right")
        d = paths.CHARTS_PATH + "/train-roc/" + relation
        file_util.ensure_dir(d)
        pyplot.savefig(d + "/" + "roc-%s.png" % prefix)
        pyplot.close()

    def try_classifier(name, classifier, prefix):
        clf = classifier.fit(X_train, y_train)
        score = clf.decision_function(X_test)

        fpr, tpr, _ = metrics.roc_curve(y_test, score)
        auc = metrics.auc(fpr, tpr)
        print("%s AUC:" % name, auc)

        plot_roc(fpr, tpr, auc, prefix)

        predicted = clf.predict(X_test)
        print("%s accuracy:" % name, numpy.mean(predicted == y_test))

        positive_probs = []
        negative_probs = []
        scores = clf.predict_proba(X_train)
        for i in range(X_train.shape[0]):
            if y_train[i]:
                positive_probs.append(scores[i][1])
            else:
                negative_probs.append(scores[i][1])
        print("Train -- positive avg:",
              numpy.mean(positive_probs),
              "negative avg:",
              numpy.mean(negative_probs))

        positive_probs = []
        negative_probs = []
        scores = clf.predict_proba(X_test)
        for i in range(X_test.shape[0]):
            if y_test[i]:
                positive_probs.append(scores[i][1])
            else:
                negative_probs.append(scores[i][1])
        print("Test -- positive avg:",
              numpy.mean(positive_probs),
              "negative avg:",
              numpy.mean(negative_probs))

        return clf

    clf = try_classifier('Logistic regression', linear_model.LogisticRegression(),
                         'logreg')

    file_util.ensure_dir(paths.MODELS_PATH)
    with open(paths.MODELS_PATH + "/" + relation + ".pkl", "wb") as f:
        pickle.dump({'classifier': clf, 'features': all_features}, f)

    #try_classifier('Linear SVM',
    #               linear_model.SGDClassifier(loss='hinge', penalty='l2',
    #                                          alpha=1e-3, n_iter=5,
    #                                          random_state=42),
    #               'linear-svm')

def main():
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('--parallelism', default=1, type=int)
    parser.add_argument('--relation', action='append')
    args = parser.parse_args()

    if args.relation:
        relations = args.relation
    else:
        relations = sample_repo.all_relations()

    pool = multiprocessing.Pool(args.parallelism)
    pool.map(train_classifier_for_relation, relations)
    #for relation in sample_repo.all_relations():
    #    train_classifier_for_relation(relation)

if __name__ == '__main__':
    main()

