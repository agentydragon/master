import json
import progressbar
from prototype.extraction import model as model_lib
from prototype.fusion import fuser as fuser_lib
from prototype.lib import file_util
from prototype.lib import flags
from prototype.lib import article_set
from prototype.lib import sample_repo
from prototype.lib import sample_generation
from prototype.lib import relations

def find_samples_in_document(relation, title):
    scored_samples = []
    # print('Processing document:', title)
    document = sample_generation.try_load_document(title)
    if not document:
        print('Cannot load document', title, ':(')
        return []

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
    flags.add_argument('--relation', action='append')
    # flags.add_argument('--json_out', required=True)
    flags.make_parser(description='TODO')
    args = flags.parse_args()

    if args.relation:
        run_on_relations = args.relation
    else:
        run_on_relations = relations.RELATIONS

    if args.article:
        articles = args.article
    else:
        # TODO: calibration set should be separate
        art_set = article_set.ArticleSet()
        train, test, calibrate = art_set.split_train_test_calibrate()
        # articles = calibrate[:100]
        articles = calibrate

    for relation in run_on_relations:
        print('Making fuser training data for', relation)

        print("Loading model for %s." % relation)
        try:
            model = model_lib.Model.load(relation)
        except Exception as e:
            print('Failed to load model for', relation, ':(')
            print(e)
            print('Skipping relation, cannot load model')
            continue

        all_samples = []
        bar = progressbar.ProgressBar(redirect_stdout=True)
        for article in bar(articles):
            samples = find_samples_in_document(relation, article)
            if samples:
                all_samples.extend(samples)

        scored_samples = []
        scores = model.predict_proba(all_samples)
        for i, sample in enumerate(all_samples):
            s = sample.subject
            r = sample.relation
            o = sample.object
            text = sample.sentence.text
            score = scores[i]
            scored_samples.append((float(score[1]), sample))

        by_relation = show_assertion_support(relation, scored_samples)
        output_dir = fuser_lib.FUSER_TRAINING_DATA_PATH
        file_util.ensure_dir(output_dir)
        output_file = output_dir + '/' + relation + '.json'
        with open(output_file, 'w') as f:
            json.dump(by_relation, f)

if __name__ == '__main__':
    main()
