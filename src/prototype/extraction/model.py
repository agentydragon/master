from src import paths
from src.prototype.extraction import feature_extraction
from src.prototype.lib import file_util
import pickle

class Model(object):
    def __init__(self, classifier, head_features_dict, relation):
        self.classifier = classifier
        self.head_features_dict = head_features_dict
        self.relation = relation

    @classmethod
    def load(cls, relation):
        with open(paths.MODELS_PATH + "/" + relation + ".pkl", "rb") as f:
            d = pickle.load(f)
            return cls(
                classifier = d['classifier'],
                head_features_dict = d['features'],
                relation = d['relation'],
            )

    def save(self):
        file_util.ensure_dir(paths.MODELS_PATH)
        with open(paths.MODELS_PATH + "/" + self.relation + ".pkl", "wb") as f:
            pickle.dump({
                'classifier': self.classifier,
                'features': self.head_features_dict,
                'relation': self.relation,
            }, f)

    def samples_to_matrix(self, samples):
        return feature_extraction.samples_to_matrix(
            samples,
            self.head_features_dict
        )

    def predict_proba(self, samples):
        matrix = self.samples_to_matrix(samples)
        scores = self.classifier.predict_proba(matrix)
        return scores
