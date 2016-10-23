from src.prototype.lib import file_util
from src.prototype.lib import article_repo
from src.prototype.lib import training_sample
from src import paths

import json
import io
import os.path

import progressbar

class SavingError(Exception):
    pass

base_dir = paths.RELATION_SAMPLES_DIR

def article_relation_to_path(title, relation):
    sanitized_articletitle = article_repo.sanitize_articletitle(title)
    first1 = sanitized_articletitle[:1]
    first2 = sanitized_articletitle[:2]
    first3 = sanitized_articletitle[:3]

    target_dir = base_dir + '/' + relation + '/' + first1 + '/' + first2 + '/' + first3
    file_util.ensure_dir(target_dir)
    return target_dir + '/' + sanitized_articletitle + '.json'

def write_relations(title, relation, samples):
    # TODO: richer samples
    # Check that there are no duplicate samples.
    # TODO!
    # if len(set(map(json.dumps, samps))) != len(samps):
    #     raise SavingError('Samples were reduced')

    with open(article_relation_to_path(title, relation), 'w') as f:
        json.dump({'samples': [sample.to_json() for sample in samples]}, f)

def load_document_samples(relations, title):
    samples = []
    for relation in relations:
        path = article_relation_to_path(title, relation)
        if os.path.isfile(path):
            with open(path) as f:
                samples.extend(list(map(training_sample.TrainingSample.from_json, json.load(f)['samples'])))
    return samples

def load_documents_samples(relation, documents):
    samples = []
    bar = progressbar.ProgressBar()
    for document in bar(documents):
        samples.extend(load_document_samples([relation], document))
    return samples

def write_article(title, samples):
    by_relation = {}
    for sample in samples:
        relation = sample.relation
        if relation not in by_relation:
            by_relation[relation] = []
        by_relation[relation].append(sample)

    for relation in by_relation:
        write_relations(title, relation, by_relation[relation])
