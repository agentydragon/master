import json
import progressbar
from prototype import feature_extraction
from prototype.lib import flags
from prototype.lib import article_set
from prototype.lib import sample_generation
from prototype.lib import wikidata
from prototype.lib import relations
from scipy import sparse
import numpy
import paths
import pickle

# load classifiers

flags.add_argument('--article', action='append')
flags.add_argument('--json_out', required=True)
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
        # print('Looking for relation', relation, '...')

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

        if len(document_samples) == 0:
            print("No samples in document.")
            return

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

def show_assertion_support():
    wikidata_client = wikidata.WikidataClient()
    by_relation = {relation: {'true': [], 'false': []} for relation in relations.RELATIONS}

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
    # TODO: wikidata queries should be optimizable here.
    bar = progressbar.ProgressBar()
    for subject, relation, object in bar(order):
        supports = support[(subject, relation, object)]
        # heading = ' '.join([(wikidata_client.get_name(subject) or '??') + ',',
        #                     wikidata_client.get_name(relation) + ',',
        #                     (wikidata_client.get_name(object) or '??')]).rjust(80)
        truth = wikidata_client.relation_exists(subject, relation, object)

        # average = sum(supports) / len(supports)
        # maximum = max(supports)
        # label = (1 if truth else 0)
        # print(average, maximum, label)

        label = ('true' if truth else 'false')
        by_relation[relation][label].append(supports)
        # by_relation[relation][subject + ';' + object] = {'supports': supports,
        #                                                  'label': (1 if truth else 0)}
        # print(heading + ':', ('+' if truth else '.'), ' ',
        #       ' '.join([('%.4f' % s) for s in reversed(sorted(supports))]))

    with open(args.json_out, 'w') as f:
        json.dump(by_relation, f)

bar = progressbar.ProgressBar(redirect_stdout=True)

if args.article:
    articles = args.article
else:
    # TODO: calibration set should be separate
    art_set = article_set.ArticleSet()
    train, test, calibrate = art_set.split_train_test_calibrate()
    # articles = calibrate[:100]
    articles = calibrate

for article in bar(articles):
    find_samples_in_document(article)

show_assertion_support()
