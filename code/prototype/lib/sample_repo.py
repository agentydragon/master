import paths
import json
from prototype.lib import file_util
import io
import os.path
from prototype.lib import article_repo
from prototype.lib import training_sample

class SavingError(Exception):
    pass

base_dir = paths.RELATION_SAMPLES_DIR

def article_relation_to_path(title, relation, positive):
    sanitized_articletitle = article_repo.sanitize_articletitle(title)
    first1 = sanitized_articletitle[:1]
    first2 = sanitized_articletitle[:2]
    first3 = sanitized_articletitle[:3]

    if positive:
        p = 'positive'
    else:
        p = 'negative'

    target_dir = base_dir + '/' + relation + '/' + p + '/' + first1 + '/' + first2 + '/' + first3
    file_util.ensure_dir(target_dir)
    return target_dir + '/' + sanitized_articletitle + '.json'

def write_relations(title, relation, samples):
    # TODO: richer samples
    # Check that there are no duplicate samples.
    # TODO!
    # if len(set(map(json.dumps, samps))) != len(samps):
    #     raise SavingError('Samples were reduced')

    positives = [sample for sample in samples if sample.positive]
    if len(positives) > 0:
        with open(article_relation_to_path(title, relation, positive=True), 'w') as f:
            json.dump({'samples': [sample.to_json() for sample in positives]}, f)

    negatives = [sample for sample in samples if not sample.positive]
    if len(negatives) > 0:
        with open(article_relation_to_path(title, relation, positive=False), 'w') as f:
            json.dump({'samples': [sample.to_json() for sample in negatives]}, f)

def write_positive_samples(relation, samples):
    with open(base_dir + '/' + relation + '/positives.json', 'w') as f:
        json.dump({'samples': [sample.to_json() for sample in samples]}, f)

def write_negative_samples(relation, samples):
    with open(base_dir + '/' + relation + '/negatives.json', 'w') as f:
        json.dump({'samples': [sample.to_json() for sample in samples]}, f)

def write_article(title, samples):
    by_relation = {}
    for sample in samples:
        relation = sample.relation
        if relation not in by_relation:
            by_relation[relation] = []
        by_relation[relation].append(sample)

    for relation in by_relation:
        write_relations(title, relation, by_relation[relation])

def load_positive_samples(relation):
    with open(base_dir + '/' + relation + '/positives.json') as f:
        batch = json.load(f)['samples']
        return list(map(training_sample.TrainingSample.from_json, batch))

def load_negative_samples(relation):
    with open(base_dir + '/' + relation + '/negatives.json') as f:
        batch = json.load(f)['samples']
        return list(map(training_sample.TrainingSample.from_json, batch))

def load_samples(relation):
    samples = []
    samples.extend(load_positive_samples(relation))
    samples.extend(load_negative_samples(relation))
    return samples

def load_negative_samples_by_articles(relation):
    samples = []
    for root, subdirs, files in os.walk(base_dir + '/' + relation + '/negative'):
        for f in files:
            filename = root + '/' + f
            try:
                with open(filename) as f:
                    batch = json.load(f)['samples']
            except ValueError as e:
                print('Cannot parse JSON file', filename, ', skipping')
                print(e)
                continue
            samples.extend(map(training_sample.TrainingSample.from_json, batch))
    return samples

def load_positive_samples_by_articles(relation):
    samples = []
    for root, subdirs, files in os.walk(base_dir + '/' + relation + '/positive'):
        for f in files:
            filename = root + '/' + f
            with open(filename) as f:
                batch = json.load(f)['samples']
            samples.extend(map(training_sample.TrainingSample.from_json, batch))
    return samples

def all_relations():
    return list(sorted(os.listdir(base_dir)))
