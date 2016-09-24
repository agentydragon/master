from prototype.lib import sample_repo
from prototype.lib import dbpedia
from prototype.lib import sample_generation
from prototype.lib import wikidata
from prototype import feature_extraction
import paths
from prototype.lib import file_util
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot
import numpy
from scipy import sparse
from sklearn import metrics
from sklearn import naive_bayes
from sklearn import cross_validation
from sklearn import linear_model

relation = 'P25'
wikidata_client = wikidata.WikidataClient()
print('Training for', relation, wikidata_client.get_name(relation))

positive_samples = sample_repo.load_positive_samples(relation)[:20]
negative_samples = []

article_titles = set(sample.sentence.origin_article
                     for sample in positive_samples)
dbpedia_client = dbpedia.DBpediaClient()
for i, title in enumerate(article_titles):
    print('Getting negative samples from', title, '(', i, '/', len(article_titles), ')')

    art = sample_generation.try_load_document(title)
    if art is None:
        continue

    positive_sentence_ids = set(sample.sentence.origin_sentence_id
                                for sample in positive_samples
                                if sample.sentence.origin_article == title)

    for sentence in art.sentences:
        if sentence.id in positive_sentence_ids:
            continue
        else:
            sentence_wrapper = sample_generation.SentenceWrapper(art,
                                                                 sentence,
                                                                 dbpedia_client)
            wikidata_ids = sentence_wrapper.get_sentence_wikidata_ids()
            for s in wikidata_ids:
                for o in wikidata_ids:
                    if sentence_wrapper.mentions_in_sentence_overlap(s, o):
                        continue

                    negative_samples.append(sentence_wrapper.make_training_sample(
                        s, relation, o, positive=False))

#relation_samples = sample_repo.load_samples(relation)
relation_samples = positive_samples + negative_samples
print('Positive:', len([sample for sample in relation_samples
                        if sample.positive]))
print('Negative:', len([sample for sample in relation_samples
                        if not sample.positive]))

print('Collecting features...')

things = list(map(feature_extraction.sample_to_features_label, relation_samples)) # [:10]
all_features = set()
for thing in things:
    all_features = all_features.union(thing[0])
all_features = list(sorted(all_features))

print('Converting to feature matrix...')

matrix = sparse.lil_matrix((len(relation_samples), len(all_features)), dtype=numpy.int8)
for i, thing in enumerate(things):
    sample_features, label = thing
    for feature in sample_features:
        matrix[i, all_features.index(feature)] = 1

print('Splitting and training.')
# print(matrix.toarray())

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
    print('Training %s...' % name)
    clf = classifier.fit(X_train, y_train)
    score = clf.decision_function(X_test)

    fpr, tpr, _ = metrics.roc_curve(y_test, score)
    auc = metrics.auc(fpr, tpr)
    print("%s AUC:" % name, auc)

    plot_roc(fpr, tpr, auc, prefix)

    predicted = clf.predict(X_test)
    print("%s accuracy:" % name, numpy.mean(predicted == y_test))

try_classifier('Logistic regression',
               linear_model.LogisticRegression(verbose=True),
               'logreg')
try_classifier('Linear SVM',
               linear_model.SGDClassifier(loss='hinge', penalty='l2',
                                          alpha=1e-3, n_iter=5,
                                          random_state=42),
               'linear-svm')

