import json
from src.prototype.lib import sample_repo
from src.prototype.lib import training_sample

last_key = None
samples = []

def flush(key):
    global last_key
    global samples
    if last_key != key:
        if len(samples) > 0:
            relation = last_key.split(':')[0]
            article = last_key[len(relation) + 1:]

            sample_repo.write_relations(article, relation, samples)
            print(last_key, len(samples))

        samples = []
        last_key = key

for line in open('/hdfs/user/prvak/ts.txt/part-r-00000', 'r'):
    key, rest = line.split('\t')
    flush(key)
    samples.append(training_sample.TrainingSample.from_json(json.loads(rest)))
flush(None)
