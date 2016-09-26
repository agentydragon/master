from prototype import feature_extraction
from prototype.lib import sample_generation
from prototype.lib import wikidata
from scipy import sparse
from sklearn import cross_validation
from sklearn import linear_model
from sklearn import metrics
from sklearn import naive_bayes
import numpy
import paths
import pickle

# load classifiers
relations = ['P106', # occupation,
             'P102', # member of political party
             'P27', # country of citizenship
             'P108', # employer
             'P25', # mother
             'P22', # father
             'P7', # brother
             'P40', # child
             ]

classifiers = {}

for relation in relations:
    try:
        with open(paths.MODELS_PATH + "/" + relation + ".pkl", "rb") as f:
            d = pickle.load(f)

        classifiers[relation] = d
    except:
        print('Failed to load classifier for', relation, ':(')
    #clf = d['classifier']
    #all_features = d['features']

document = sample_generation.try_load_document('Albert Einstein')

scored_samples = []

for relation in classifiers:
    print('Looking for relation', relation, '...')

    document_samples = []
    for sentence in document.sentences:
        sentence_wrapper = sample_generation.SentenceWrapper(
            document,
            sentence,
        )
        wikidata_ids = sentence_wrapper.get_sentence_wikidata_ids()

        sentence_samples = []
        for e1 in wikidata_ids:
            for e2 in wikidata_ids:
                if e1 == e2:
                    continue
                sample = sentence_wrapper.make_training_sample(e1, relation, e2,
                                                               positive=None)
                sentence_samples.append(sample)

        document_samples.extend(sentence_samples)

    clf = classifiers[relation]['classifier']
    all_features = classifiers[relation]['features']

    matrix = sparse.lil_matrix((len(document_samples), len(all_features)), dtype=numpy.int8)
    for i, sample in enumerate(document_samples):
        features = feature_extraction.sample_to_features(sample)
        for feature in features:
            if feature not in all_features:
                continue
            else:
                matrix[i, all_features.index(feature)] = 1

    scores = clf.predict_proba(matrix)
    #print(scores)

    for i, sample in enumerate(document_samples):
        s = sample.subject
        r = sample.relation
        o = sample.object
        text = sample.sentence.text
        score = scores[i]
        #print(score)
        scored_samples.append((float(score[1]), (s, r, o, text)))

wikidata_client = wikidata.WikidataClient()
scored_samples = reversed(sorted(scored_samples))
for score, stuff in scored_samples:
    s, r, o, text = stuff
    truth = wikidata_client.relation_exists(s, r, o)
    print(score, text,
          wikidata_client.get_name(s),
          wikidata_client.get_name(r),
          wikidata_client.get_name(o),
          truth)
