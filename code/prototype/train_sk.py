from prototype.lib import sample_repo
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

# TODO: train-test split

X_train, X_test, y_train, y_test = cross_validation.train_test_split(
    matrix, target, test_size=0.33, random_state=42)

clf = linear_model.LogisticRegression().fit(X_train, y_train)
score = clf.decision_function(X_test)
print(len(y_test))
print(y_test)
print(len(score))
print(score)

fpr, tpr, _ = metrics.roc_curve(y_test, score)
auc = metrics.auc(fpr, tpr)
print("Logistic regression AUC:", auc)

def plot_roc(fpr, tpr, auc, prefix):
    pyplot.figure()
    pyplot.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % auc)
    pyplot.plot([0, 1], [0, 1], 'k--')
    pyplot.xlim([0.0, 1.0])
    pyplot.ylim([0.0, 1.0])
    pyplot.xlabel('False Positive Rate')
    pyplot.xlabel('True Positive Rate')
    pyplot.legend(loc="lower right")
    pyplot.savefig("roc-%s.png" % prefix)

print(fpr, tpr)
plot_roc(fpr, tpr, auc, "logreg")

predicted = clf.predict(X_test)
print("Logistic regression accuracy:", numpy.mean(predicted == y_test))

#clf = linear_model.SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3,
#                                 n_iter=5, random_state=42).fit(X_train, y_train)
#score = clf.decision_function(X_test)

#fpr, tpr, _ = metrics.roc_curve(y_test, score)
#auc = metrics.auc(fpr, tpr)
#print("Linear SVM AUC:", auc)
#
#plot_roc(fpr, tpr, auc, "linear-svm")
#
#predicted = clf.predict(X_test)
#print("Linear SVM accuracy:", numpy.mean(predicted == y_test))
