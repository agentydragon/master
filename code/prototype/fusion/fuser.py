import paths
import numpy
from prototype.lib import file_util
import pickle

FUSER_MODELS_PATH = paths.MODELS_PATH + "/fusion"
FUSER_TRAINING_DATA_PATH = paths.WORK_DIR + '/fuser-train'

def sentence_scores_to_features(sentence_scores):
    features = [
        # math.log(len(sentence_scores)),
        # math.sqrt(len(sentence_scores)),
        sum(sentence_scores) / len(sentence_scores),
    ]
    # TODO: Idea: share of sentences with p>=X for different values of X
    return features

class Fuser(object):
    def __init__(self, relation, classifier):
        self.relation = relation
        self.classifier = classifier

    @classmethod
    def load(cls, relation):
        with open(FUSER_MODELS_PATH + '/' + relation + ".pkl", "rb") as f:
            d = pickle.load(f)
            return cls(
                classifier = d['classifier'],
                relation = d['relation'],
            )

    def save(self):
        file_util.ensure_dir(FUSER_MODELS_PATH)
        with open(FUSER_MODELS_PATH + '/' + self.relation + ".pkl", "wb") as f:
            pickle.dump({
                'classifier': self.classifier,
                'relation': self.relation,
            }, f)

    def predict_proba(self, sentence_scores):
        features = sentence_scores_to_features(numpy.array(sentence_scores))
        return self.classifier.predict_proba(features)[0][1]
