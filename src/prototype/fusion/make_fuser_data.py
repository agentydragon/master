import json
import progressbar
from src.prototype.extraction import model as model_lib
from src.prototype.fusion import fuser as fuser_lib
from src.prototype.lib import file_util
from src.prototype.lib import flags
from src.prototype.lib import sample_repo
from src.prototype.lib import relations


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
    flags.make_parser(description='TODO')
    args = flags.parse_args()

    if args.relation:
        run_on_relations = args.relation
    else:
        run_on_relations = relations.RELATIONS

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

        no_samples = 0
        bar = progressbar.ProgressBar(redirect_stdout=True)
        all_samples = sample_repo.load_samples(relation, 'calibrate')
        print("number of samples:", len(all_samples))
        assert len(all_samples) > 1, "no samples!"

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
