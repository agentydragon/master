from src.prototype import feature_extraction
from src.prototype.lib import flags
from src.prototype.lib import sample_generation
from src.prototype.lib import wikidata
from src.prototype.lib import relations
from src import paths
from scipy import sparse
import numpy
import pickle

# load classifiers

flags.add_argument('--article', action='append')
flags.make_parser(description='TODO')
args = flags.parse_args()

print("Loading classifiers.")
classifiers = {}
for relation in relations.RELATIONS:
    try:
        with open(paths.MODELS_PATH + "/" + relation + ".pkl", "rb") as f:
            d = pickle.load(f)

        classifiers[relation] = d
    except Exception as e:
        print('Failed to load classifier for', relation, ':(')
        print(e)
    #clf = d['classifier']
    #all_features = d['features']

scored_samples = []

def find_samples_in_document(title):
    print('Processing document:', title)
    document = sample_generation.try_load_document(title)
    if not document:
        print('Cannot load :(')
        return

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
                    matrix[i, all_features[feature]] = 1

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

def show_sentence_scores():
    wikidata_client = wikidata.WikidataClient()
    smpls = reversed(sorted(scored_samples))

    for score, stuff in smpls:
        s, r, o, text = stuff
        truth = wikidata_client.relation_exists(s, r, o)
        print(score, text,
              wikidata_client.get_name(s),
              wikidata_client.get_name(r),
              wikidata_client.get_name(o),
              truth)

def show_assertion_support():
    wikidata_client = wikidata.WikidataClient()

    # key: (subject, relation, object)
    # value: [support1, support2, ...]
    support = {}
    for certainty, tuple in scored_samples:
        subject, relation, object, text = tuple
        key = (subject, relation, object)
        if key not in support:
            support[key] = []
        support[key].append(certainty)

    # Order by average support.
    order = sorted(support.keys(),
                   key=lambda k: sum(support[k]) / len(support[k]),
                   reverse=True)
    for subject, relation, object in order:
        supports = support[(subject, relation, object)]
        heading = ' '.join([(wikidata_client.get_name(subject) or '??') + ',',
                            wikidata_client.get_name(relation) + ',',
                            (wikidata_client.get_name(object) or '??')]).rjust(80)
        truth = wikidata_client.relation_exists(subject, relation, object)
        print(heading + ':', ('+' if truth else '.'), ' ',
              ' '.join([('%.4f' % s) for s in reversed(sorted(supports))]))

for article in args.article:
    find_samples_in_document(article)
show_assertion_support()
