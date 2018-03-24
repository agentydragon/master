from src.prototype.lib import file_util
from src.prototype.lib import article_repo
from src.prototype.lib import training_sample
from src import paths

import glob
import json
import io
import os.path

import progressbar

base_dir = paths.RELATION_SAMPLES_DIR

def load_samples(relation, s):
    samples = []
    bar = progressbar.ProgressBar()
    for filename in bar(glob.glob(base_dir + '/' + relation + '/' + s + '-r-*')):
        with open(filename, 'r') as f:
            for line in f:
                j = line[len(line.split('\t')[0])+1:]
                samples.append(training_sample.TrainingSample.from_json(json.loads(j)))
    return samples
