import json
import progressbar
from prototype import feature_extraction
from prototype.lib import file_util
from prototype.lib import flags
from prototype.lib import article_set
from prototype.lib import sample_repo
from prototype.lib import sample_generation
from prototype.lib import relations
import paths
import pickle

def load_classifier(relation):
    print("Loading classifiers.")
    try:
        with open(paths.MODELS_PATH + "/" + relation + ".pkl", "rb") as f:
            return pickle.load(f)
    except Exception as e:
        print('Failed to load classifier for', relation, ':(')
        print(e)
        return None

def find_samples_in_document(relation, classifier, title):
    scored_samples = []
    # print('Processing document:', title)
    document = sample_generation.try_load_document(title)
    if not document:
        print('Cannot load :(')
        return

    document_samples = sample_repo.load_document_samples(
        relations = [relation],
        title = title
    )
    if len(document_samples) == 0:
        # print("No samples in document.")
        return
    return document_samples

def show_assertion_support(relation, scored_samples):
    by_relation = {'true': [], 'false': []}

    # key: (subject, relation, object)
    # value: [support1, support2, ...]
    truths = {}

    support = {}
    for certainty, sample in scored_samples:
        key = (sample.subject, sample.relation, sample.object)
        if key not in support:
            support[key] = []
        support[key].append(certainty)

        if key not in truths:
            truths[key] = sample.positive
        else:
            assert truths[key] == sample.positive

    for subject, r, object in support.keys():
        assert r == relation
        key = (subject, relation, object)
        supports = support[key]
        truth = truths[key]
        truth_label = ('true' if truth else 'false')
        by_relation[truth_label].append(supports)
    return by_relation

def main():
    flags.add_argument('--article', action='append')
    # flags.add_argument('--json_out', required=True)
    flags.make_parser(description='TODO')
    args = flags.parse_args()

    if args.article:
        articles = args.article
    else:
        # TODO: calibration set should be separate
        art_set = article_set.ArticleSet()
        train, test, calibrate = art_set.split_train_test_calibrate()
        # articles = calibrate[:100]
        articles = calibrate

    for relation in relations.RELATIONS:
        print('Making fuser training data for', relation)
        classifier = load_classifier(relation)
        if not classifier:
            print('Skipping relation, cannot load classifier')
            continue

        all_samples = []
        bar = progressbar.ProgressBar(redirect_stdout=True)
        for article in bar(articles):
            samples = find_samples_in_document(relation, classifier, article)
            if samples:
                all_samples.extend(samples)

        clf = classifier['classifier']
        head_feature_dict = classifier['features']
        matrix = feature_extraction.samples_to_matrix(
            all_samples,
            head_feature_dict
        )

        scored_samples = []
        scores = clf.predict_proba(matrix)
        for i, sample in enumerate(all_samples):
            s = sample.subject
            r = sample.relation
            o = sample.object
            text = sample.sentence.text
            score = scores[i]
            scored_samples.append((float(score[1]), sample))

        by_relation = show_assertion_support(relation, scored_samples)
        output_dir = paths.WORK_DIR + '/fuser_data'
        file_util.ensure_dir(output_dir)
        output_file = output_dir + '/' + relation + '.json'
        with open(output_file, 'w') as f:
            json.dump(by_relation, f)

if __name__ == '__main__':
    main()
