from prototype.lib import sample_repo
import random
import nltk
import nltk.classify.decisiontree
import nltk.classify.maxent

relations = [
    'P25', # mother
    'P22', # father
    'P7', # brother
    'P40', # child
    'P26', # spouse
]

#     'P108', # employer
#     'P710', # participant
#     'P463', # member of
#     'P27', # country of citizenship
#     'P36', # capital
#     'P31', # instance of
#     'P1066', # student of
#     'P551', # residence
#     'P112', # founder
#     'P115', # follows
#     'P175', # performer
#     'P457', # member of political party
#     'P50', # author
#     'P19', # place of birth
#     'P361', # part of
#     'P86', # composer
#     'P57', # director
#     'P463', # member of
#     'P69', # educated at
#     'P159', # headquarters location
#     'P140', # religion
#     'P800', # notable work
# ]

# relations = sample_repo.all_relations()

def sample_to_features_label(sample):
    features = {}
    for i, token in enumerate(sample.sentence.tokens):
        # debias
        if i in sample.subject_token_indices:
            continue
        if i in sample.object_token_indices:
            continue

        features['lemma_' + token.lemma.lower()] = 1
        word = sample.sentence.text[token.start_offset:token.end_offset].lower()
        features['word_' + word] = 1

    # window before subject
    for i in range(-2, 0):
        idx = min(sample.subject_token_indices) - i
        if idx not in range(len(sample.sentence.tokens)):
            continue
        features['subject_window_%d_lemma_%s' % (i, token.lemma)] = 1
        word = sample.sentence.text[token.start_offset:token.end_offset].lower()
        features['subject_window_%d_word_%s' % (i, word)] = 1

    # window before object
    for i in range(-2, 0):
        idx = min(sample.object_token_indices) - i
        if idx not in range(len(sample.sentence.tokens)):
            continue
        features['object_window_%d_lemma_%s' % (i, token.lemma)] = 1
        word = sample.sentence.text[token.start_offset:token.end_offset].lower()
        features['object_window_%d_word_%s' % (i, word)] = 1

    # window after subject
    for i in range(1, 3):
        idx = max(sample.subject_token_indices) + i
        if idx not in range(len(sample.sentence.tokens)):
            continue
        features['subject_window_%d_lemma_%s' % (i, token.lemma)] = 1
        word = sample.sentence.text[token.start_offset:token.end_offset].lower()
        features['subject_window_%d_word_%s' % (i, word)] = 1

    # window after object
    for i in range(1, 3):
        idx = max(sample.object_token_indices) + i
        if idx not in range(len(sample.sentence.tokens)):
            continue
        features['object_window_%d_lemma_%s' % (i, token.lemma)] = 1
        word = sample.sentence.text[token.start_offset:token.end_offset].lower()
        features['object_window_%d_word_%s' % (i, word)] = 1

    return (features, sample.relation)

#samples = sample_repo.load_samples(mother)
#for sample in samples:
#    lemmas = []
#    for i, token in enumerate(sample.sentence.tokens):
#        lemmas.append(token.lemma)
#    print(" ".join(lemmas))

def cull_uninformative_features(samples):
    feature_counts = {}
    for sample in samples:
        for feature in list(sample[0].keys()):
            if feature not in feature_counts:
                feature_counts[feature] = 0
            feature_counts[feature] += 1

    min_feature_occurrences = 10

    for sample in samples:
        for feature in list(sample[0].keys()):
            if feature_counts[feature] < min_feature_occurrences:
                del sample[0][feature]

samples = []
for relation in relations:
    print('Loading relation', relation, '...')
    relation_samples = sample_repo.load_samples(relation)
    for sample in relation_samples:
        samples.append(sample_to_features_label(sample))
    print(len(relation_samples))

random.shuffle(samples)
cull_uninformative_features(samples)

print("Samples:", len(samples))

n_train = round(len(samples) * 0.5)
train = samples[:n_train]
test = samples[n_train:]
print("N training samples:", len(train), "test:", len(test))

print('Training naive Bayes...')
classifier = nltk.NaiveBayesClassifier.train(train)
classifier.show_most_informative_features(10)
print('Accuracy:', nltk.classify.accuracy(classifier, test))

print('Training decision tree...')
classifier = nltk.classify.decisiontree.DecisionTreeClassifier.train(
    train, depth_cutoff=4, binary=True)
# classifier.show_most_informative_features(10)
print('Accuracy:', nltk.classify.accuracy(classifier, test))

print('Training maxent...')
classifier = nltk.classify.maxent.MaxentClassifier.train(train)
# classifier.show_most_informative_features(10)
print('Accuracy:', nltk.classify.accuracy(classifier, test))
