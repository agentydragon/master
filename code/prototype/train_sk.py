from prototype.lib import sample_repo
from py import paths
from py import file_util
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot
import numpy
from scipy import sparse
from sklearn import metrics
from sklearn import naive_bayes
from sklearn import cross_validation
from sklearn import linear_model

def sample_to_features_label(sample):
    features = set()
    for i, token in enumerate(sample.sentence.tokens):
        # debias
        if i in sample.subject_token_indices:
            continue
        if i in sample.object_token_indices:
            continue

        features.add('lemma_' + token.lemma.lower())
        word = sample.sentence.text[token.start_offset:token.end_offset].lower()
        features.add('word_' + word)

    # window before subject
    for i in range(-2, 0):
        idx = min(sample.subject_token_indices) - i
        if idx not in range(len(sample.sentence.tokens)):
            continue
        features.add('subject_window_%d_lemma_%s' % (i, token.lemma))
        word = sample.sentence.text[token.start_offset:token.end_offset].lower()
        features.add('subject_window_%d_word_%s' % (i, word))

    # window before object
    for i in range(-2, 0):
        idx = min(sample.object_token_indices) - i
        if idx not in range(len(sample.sentence.tokens)):
            continue
        features.add('object_window_%d_lemma_%s' % (i, token.lemma))
        word = sample.sentence.text[token.start_offset:token.end_offset].lower()
        features.add('object_window_%d_word_%s' % (i, word))

    # window after subject
    for i in range(1, 3):
        idx = max(sample.subject_token_indices) + i
        if idx not in range(len(sample.sentence.tokens)):
            continue
        features.add('subject_window_%d_lemma_%s' % (i, token.lemma))
        word = sample.sentence.text[token.start_offset:token.end_offset].lower()
        features.add('subject_window_%d_word_%s' % (i, word))

    # window after object
    for i in range(1, 3):
        idx = max(sample.object_token_indices) + i
        if idx not in range(len(sample.sentence.tokens)):
            continue
        features.add('object_window_%d_lemma_%s' % (i, token.lemma))
        word = sample.sentence.text[token.start_offset:token.end_offset].lower()
        features.add('object_window_%d_word_%s' % (i, word))

    if min(sample.subject_token_indices) < min(sample.object_token_indices):
        features.add('subject_first')
    else:
        features.add('object_first')

    return (features, sample.positive)

relation_samples = sample_repo.load_samples('P25')
print('Positive:', len([sample for sample in relation_samples if
                       sample.positive]))
print('Negative:', len([sample for sample in relation_samples if not
                       sample.positive]))

things = list(map(sample_to_features_label, relation_samples)) # [:10]
all_features = set()
for thing in things:
    all_features = all_features.union(thing[0])
all_features = list(sorted(all_features))

matrix = sparse.lil_matrix((len(relation_samples), len(all_features)), dtype=numpy.int8)
for i, thing in enumerate(things):
    for feature in thing[0]:
        matrix[i, all_features.index(feature)] = 1

print(matrix.toarray())

target = [thing[1] for thing in things]
X_train, X_test, y_train, y_test = cross_validation.train_test_split(
    matrix, target, test_size=0.33, random_state=42)

def plot_roc(fpr, tpr, auc, prefix):
    pyplot.figure()
    pyplot.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % auc)
    pyplot.plot([0, 1], [0, 1], 'k--')
    pyplot.xlim([0.0, 1.0])
    pyplot.ylim([0.0, 1.0])
    pyplot.xlabel('False Positive Rate')
    pyplot.ylabel('True Positive Rate')
    pyplot.legend(loc="lower right")
    d = paths.CHARTS_PATH + "/train-roc"
    file_util.ensure_dir(d)
    pyplot.savefig(d + "/" + "roc-%s.png" % prefix)

def try_classifier(name, classifier, prefix):
    clf = classifier.fit(X_train, y_train)
    score = clf.decision_function(X_test)

    fpr, tpr, _ = metrics.roc_curve(y_test, score)
    auc = metrics.auc(fpr, tpr)
    print("%s AUC:" % name, auc)

    plot_roc(fpr, tpr, auc, prefix)

    predicted = clf.predict(X_test)
    print("%s accuracy:" % name, numpy.mean(predicted == y_test))

try_classifier('Logistic regression', linear_model.LogisticRegression(),
               'logreg')
try_classifier('Linear SVM',
               linear_model.SGDClassifier(loss='hinge', penalty='l2',
                                          alpha=1e-3, n_iter=5,
                                          random_state=42),
               'linear-svm')

