from src.prototype.lib import file_util
from src.prototype.lib import article_repo
from src.prototype.lib import training_sample
from src import paths

import json
import io
import os.path

import progressbar

base_dir = paths.RELATION_SAMPLES_DIR

def load_samples(relation, s):
    samples = []
    with open(base_dir + '/' + relation + 'S' + s + '-r-00000', 'r') as f:
        for line in f:
            j = line[len(line.split('\t')[0])+1:]
            samples.append(training_sample.TrainingSample.from_json(json.loads(j)))
    return samples
