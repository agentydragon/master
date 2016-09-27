from prototype import feature_extraction
from prototype.lib import article_set
from prototype.lib import flags
from prototype.lib import sample_repo
from prototype.lib import wikidata
from sklearn import linear_model
from sklearn import metrics
import numpy

def train_classifier_for_relation(relation, relation_name):
    print('Training classifier for relation:',
          relation, relation_name)

    print('Loading samples...')
    relation_samples = sample_repo.load_samples(relation)
    positive_count = len([s for s in relation_samples if s.positive])
    negative_count = len([s for s in relation_samples if not s.positive])
    print('Positive:', positive_count)
    print('Negative:', negative_count)

    if positive_count < 10 or negative_count < 10:
        print('Too few samples to train for', relation, '.')
        return

    print('Collecting features...')
    things = feature_extraction.samples_to_features_labels(relation_samples)
    feature_counts = feature_extraction.get_feature_counts(things)
    head_features_dict = feature_extraction.get_head_features(feature_counts, relation_samples)

    print('Splitting train/test...')

    train_articles, test_articles = article_set.ArticleSet().split_train_test()
    train_samples, test_samples = feature_extraction.split_samples_to_train_test(
        relation_samples,
        train_articles = train_articles,
        test_articles = test_articles
    )

    print('Converting to feature matrix...')
    X_train, y_train = feature_extraction.samples_to_matrix_target(train_samples, head_features_dict)
    X_test, y_test = feature_extraction.samples_to_matrix_target(test_samples, head_features_dict)

    print('Splitting and training.')

    def try_classifier(name, classifier, prefix):
        print('Training %s...' % name)
        clf = classifier.fit(X_train, y_train)
        score = clf.decision_function(X_test)

        fpr, tpr, _ = metrics.roc_curve(y_test, score)
        auc = metrics.auc(fpr, tpr)
        print("%s AUC:" % name, auc)

        feature_extraction.plot_roc(fpr, tpr, auc, prefix, relation=relation,
                                    relation_name=relation_name)

        predicted = clf.predict(X_test)
        print("%s accuracy:" % name, numpy.mean(predicted == y_test))

        return clf

    clf = try_classifier('Logistic regression',
                         linear_model.LogisticRegression(verbose=True),
                         'logreg')
    feature_extraction.write_model(relation, clf, head_features_dict)

    #try_classifier('Linear SVM',
    #               linear_model.SGDClassifier(loss='hinge', penalty='l2',
    #                                          alpha=1e-3, n_iter=5,
    #                                          random_state=42),
    #               'linear-svm')

def main():
    flags.add_argument('--relation', action='append')
    flags.make_parser(description='TODO')
    args = flags.parse_args()

    if args.relation:
        relations = args.relation
    else:
        assert False
        # relations = sample_repo.all_relations()

    wikidata_client = wikidata.WikidataClient()

    for relation in relations:
        relation_name = wikidata_client.get_name(relation)
        train_classifier_for_relation(relation, relation_name)

if __name__ == '__main__':
    main()

