import json
from py import file_util
import io
import os.path
from prototype.lib import article_repo

base_dir = '/storage/brno7-cerit/home/prvak/data/relation-samples'

def article_relation_to_path(title, relation):
    sanitized_articletitle = article_repo.sanitize_articletitle(title)
    first1 = sanitized_articletitle[:1]
    first2 = sanitized_articletitle[:2]
    first3 = sanitized_articletitle[:3]
    target_dir = base_dir + '/' + relation + '/positive/' + first1 + '/' + first2 + '/' + first3
    file_util.ensure_dir(target_dir)
    return target_dir + '/' + sanitized_articletitle + '.json'

def write_relations(title, relation, samples):
    # TODO: richer samples
    samps = []
    for sample in samples:
        samps.append({'subject': sample[0], 'object': sample[1], 'sentence': sample[2]})
    with open(article_relation_to_path(title, relation), 'w') as f:
        json.dump({'samples': samps}, f)

def write_article(title, samples):
    for relation in samples.keys():
        write_relations(title, relation, samples[relation])
