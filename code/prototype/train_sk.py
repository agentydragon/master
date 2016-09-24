from prototype.lib import sample_repo
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

art_set = article_set.ArticleSet()
train_articles, test_articles = art_set.split_train_test()

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
        print('cannot load document')
        continue

    positive_sentence_ids = set(sample.sentence.origin_sentence_id
                                for sample in positive_samples
                                if sample.sentence.origin_article == title)
    print('positive sentence IDs:', positive_sentence_ids)

    from_article = []
    for sentence in art.sentences:
        if sentence.id in positive_sentence_ids:
            # print('Sentence', sentence.id, ': is positive...')
            continue
        else:
            sentence_wrapper = sample_generation.SentenceWrapper(art,
                                                                 sentence,
                                                                 dbpedia_client)
            wikidata_ids = sentence_wrapper.get_sentence_wikidata_ids()
            # print('Sentence', sentence.id, ':', len(wikidata_ids), 'entities')
            for s in wikidata_ids:
                for o in wikidata_ids:
                    if sentence_wrapper.mentions_in_sentence_overlap(s, o):
                        continue

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

print('Converting to feature matrix...')

def samples_to_matrix_target(samples):
    things = list(map(feature_extraction.sample_to_features_label, samples)) # [:10]
    matrix = sparse.lil_matrix((len(things), len(all_features)), dtype=numpy.int8)
    for i, thing in enumerate(things):
        sample_features, label = thing
        for feature in sample_features:
            if feature in dcts:
                matrix[i, dcts[feature]] = 1
    target = [thing[1] for thing in things]
    return matrix, target

train_samples = []
test_samples = []
for sample in relation_samples:
    if sample.sentence.origin_article in train_articles:
        train_samples.append(sample)
    if sample.sentence.origin_article in test_articles:
        test_samples.append(sample)

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

