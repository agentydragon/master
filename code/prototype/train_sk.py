from prototype.lib import sample_repo
import argparse
import time
from prototype.lib import article_set
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

from prototype.lib import zk

#zk.start()

parser = argparse.ArgumentParser(description='TODO')
parser.add_argument('--relation', default='P25')
parser.add_argument('--max_pos', default=None, type=int)
args = parser.parse_args()

relation = args.relation

art_set = article_set.ArticleSet()
train_articles, test_articles = art_set.split_train_test()

wikidata_client = wikidata.WikidataClient()
print('Training for', relation, wikidata_client.get_name(relation))

positive_samples = sample_repo.load_positive_samples(relation)
if args.max_pos:
    positive_samples = positive_samples[:args.max_pos]
negative_samples = []

article_titles = set(sample.sentence.origin_article
                     for sample in positive_samples)
dbpedia_client = dbpedia.DBpediaClient()
for i, title in enumerate(article_titles):
    print('Getting negative samples from', title, '(', i, '/', len(article_titles), ')')

    art = sample_generation.try_load_document(title)
    if art is None:
        print('cannot load document')
        continue

    positives = set((sample.sentence.origin_sentence_id, sample.subject, sample.object)
                    for sample in positive_samples
                    if sample.sentence.origin_article == title)
    #print('positive sentence IDs:', positive_sentence_ids)

    from_article = []
    for sentence in art.sentences:
        sentence_wrapper = sample_generation.SentenceWrapper(art,
                                                             sentence,
                                                             dbpedia_client)
        wikidata_ids = sentence_wrapper.get_sentence_wikidata_ids()
        # print('Sentence', sentence.id, ':', len(wikidata_ids), 'entities')
        for s in wikidata_ids:
            for o in wikidata_ids:
                if sentence_wrapper.mentions_in_sentence_overlap(s, o):
                    continue

                if (sentence.id, s, o) not in positives:
                    from_article.append(sentence_wrapper.make_training_sample(
                        s, relation, o, positive=False))
    print('Collected', len(from_article))
    negative_samples.extend(from_article)


#relation_samples = sample_repo.load_samples(relation)
relation_samples = positive_samples + negative_samples
print('Positive:', len([sample for sample in relation_samples
                        if sample.positive]))
print('Negative:', len([sample for sample in relation_samples
                        if not sample.positive]))

print('Collecting features...')

all_features = {}
things = list(map(feature_extraction.sample_to_features_label, relation_samples)) # [:10]
print("Converted")
for thing in things:
    sample_features, label = thing
    for feature in sample_features:
        if feature not in all_features:
            all_features[feature] = 0
        all_features[feature] += 1

# Drop tail features.
enough = {feature for feature in all_features if all_features[feature] >= 5}

all_features=sorted(list(enough))
dcts = {}
for i, f in enumerate(all_features):
    dcts[f] = i
#all_features = list(sorted(all_features.keys()))
#all_features = list(sorted(all_features))

def samples_to_matrix_target(samples):
    things = list(map(feature_extraction.sample_to_features_label, samples)) # [:10]
    # matrix = sparse.lil_matrix((len(things), len(all_features)), dtype=numpy.int8)
    matrix = sparse.coo_matrix((len(things), len(all_features)), dtype=numpy.int8)

    print('converting', len(samples), 'samples to matrix,', len(all_features), 'features')
    fullstart = datetime.datetime.now()
    start = datetime.datetime.now()

    for i, thing in enumerate(things):
        if i % 100 == 0:
            if datetime.datetime.now() - start > datetime.timedelta(seconds = 5):
                print('elapsed:', (datetime.datetime.now() - fullstart).seconds, ', done:', i, 'samples')
                start = datetime.datetime.now()

        sample_features, label = thing
        sample_features = set(sample_features).intersect(dcts.keys())
        sample_features = sorted(sample_features, key=lambda f: dcts[f])
        for feature in sample_features:
            matrix[i, dcts[feature]] = 1
    target = [thing[1] for thing in things]
    return matrix, target

print('Splitting train/test...')

train_samples = []
test_samples = []
for sample in relation_samples:
    if sample.sentence.origin_article in train_articles:
        train_samples.append(sample)
    if sample.sentence.origin_article in test_articles:
        test_samples.append(sample)

print('Converting to feature matrix...')

X_train, y_train = samples_to_matrix_target(train_samples)
X_test, y_test = samples_to_matrix_target(test_samples)

print('Splitting and training.')
# print(matrix.toarray())

#X_train, X_test, y_train, y_test = cross_validation.train_test_split(
#    matrix, target, test_size=0.33, random_state=42)

def plot_roc(fpr, tpr, auc, prefix):
    pyplot.figure()
    pyplot.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % auc)
    pyplot.plot([0, 1], [0, 1], 'k--')
    pyplot.xlim([0.0, 1.0])
    pyplot.ylim([0.0, 1.0])
    pyplot.xlabel('False Positive Rate')
    pyplot.ylabel('True Positive Rate')
    pyplot.legend(loc="lower right")
    d = paths.CHARTS_PATH + "/train-roc/" + relation
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

