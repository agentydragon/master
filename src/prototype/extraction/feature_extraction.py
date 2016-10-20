from src.prototype.lib import file_util
from src import paths
import numpy
from scipy import sparse
import progressbar

def sentence_bag_of_words_features(sample):
    features = set()
    for i, token in enumerate(sample.sentence.tokens):
        # debias
        if i in sample.subject_token_indices:
            continue
        if i in sample.object_token_indices:
            continue

        features.add('lemma_' + token.lemma.lower())
        word = sample.sentence.text[token.start_offset:token.end_offset].lower()
        features.add('word_' + word)
    return features

def window_features(prefix, indices, sample):
    features = set()
    # window before
    for i in range(-2, 0):
        idx = min(indices) - i
        if idx not in range(len(sample.sentence.tokens)):
            continue
        token = sample.sentence.tokens[idx]
        features.add(prefix + '_window_%d_lemma_%s' % (i, token.lemma))
        word = sample.sentence.text[token.start_offset:token.end_offset].lower()
        features.add(prefix + '_window_%d_word_%s' % (i, word))
    # window after
    for i in range(1, 3):
        idx = max(indices) + i
        if idx not in range(len(sample.sentence.tokens)):
            continue
        token = sample.sentence.tokens[idx]
        features.add(prefix + '_window_%d_lemma_%s' % (i, token.lemma))
        word = sample.sentence.text[token.start_offset:token.end_offset].lower()
        features.add(prefix + '_window_%d_word_%s' % (i, word))
    return features

def sample_to_features(sample):
    features = set()
    # bag-of-words features
    features = features.union(sentence_bag_of_words_features(sample))

    # POS & NER tags for subject, object
    for i in sample.subject_token_indices:
        features.add('subject_pos_' + sample.sentence.tokens[i].pos)
        features.add('subject_ner_' + sample.sentence.tokens[i].ner)

    for i in sample.object_token_indices:
        features.add('object_pos_' + sample.sentence.tokens[i].pos)
        features.add('object_ner_' + sample.sentence.tokens[i].ner)

    # subject window
    subject_window = window_features('subject', sample.subject_token_indices, sample)
    features = features.union(subject_window)
    # object window
    object_window = window_features('object', sample.object_token_indices, sample)
    features = features.union(object_window)

    if min(sample.subject_token_indices) < min(sample.object_token_indices):
        features.add('subject_first')
    else:
        features.add('object_first')

    return features

def samples_to_all_features(samples):
    return map(sample_to_features, samples)

def get_feature_counts(features):
    all_features = {}
    print("Counting features...")
    for sample_features in features:
        for feature in sample_features:
            if feature not in all_features:
                all_features[feature] = 0
            all_features[feature] += 1
    print("Counted")
    return all_features

def get_head_features(feature_counts, relation_samples):
    min_occurences = len(relation_samples) / 10000
    print('min_occurences:', min_occurences)
    head_features = {feature for feature in feature_counts if feature_counts[feature] >= min_occurences}
    head_features = sorted(list(head_features))
    dcts = {}
    for i, f in enumerate(head_features):
        dcts[f] = i
    return dcts

def samples_to_matrix(samples, head_feature_dict):
    verbose = (len(samples) > 10000)

    if verbose:
        print('converting', len(samples), 'samples to matrix,',
              len(head_feature_dict), 'features')
    features = samples_to_all_features(samples)
    rows = []
    cols = []
    #data = []

    enum = features
    if verbose:
        bar = progressbar.ProgressBar(max_value = len(samples))
        enum = bar(enum)

    key_set = set(head_feature_dict.keys())
    for i, sample_features in enumerate(enum):
        f = set(sample_features) & key_set
        rows.extend([i] * len(f))
        cols.extend(head_feature_dict[x] for x in f)
        #data.extend([1] * len(f))
    # matrix = sparse.lil_matrix((len(features_labels), len(all_features)),
    #                            dtype=numpy.int8)
    # matrix = sparse.coo_matrix((len(features_labels), len(all_features)),
    #                            dtype=numpy.int8)
    #data = (1 for _ in range(len(rows)))
    data = [1] * len(rows)
    matrix = sparse.coo_matrix(
        (data,
         (rows, cols)),
        shape=(len(samples), len(head_feature_dict)),
        dtype=numpy.int8
    )
    return matrix

def samples_to_matrix_target(samples, head_feature_dict):
    matrix = samples_to_matrix(samples, head_feature_dict)
    target = [sample.positive for sample in samples]
    return matrix, target

# Split normally:
# matrix, target = feature_extraction.samples_to_matrix_target(relation_samples, head_feature_dict)
# X_train, X_test, y_train, y_test = cross_validation.train_test_split(
#     matrix, target, test_size=0.33, random_state=42)

#        positive_probs = []
#        negative_probs = []
#        scores = clf.predict_proba(X_train)
#        for i in range(X_train.shape[0]):
#            if y_train[i]:
#                positive_probs.append(scores[i][1])
#            else:
#                negative_probs.append(scores[i][1])
#        print("Train -- positive avg:",
#              numpy.mean(positive_probs),
#              "negative avg:",
#              numpy.mean(negative_probs))
#
#        positive_probs = []
#        negative_probs = []
#        scores = clf.predict_proba(X_test)
#        for i in range(X_test.shape[0]):
#            if y_test[i]:
#                positive_probs.append(scores[i][1])
#            else:
#                negative_probs.append(scores[i][1])
#        print("Test -- positive avg:",
#              numpy.mean(positive_probs),
#              "negative avg:",
#              numpy.mean(negative_probs))
