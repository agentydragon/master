from prototype.lib import sample_repo
from prototype import feature_extraction
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
    relation_samples = list(filter(lambda sample: sample.positive, relation_samples))
    for sample in relation_samples:
        samples.append(feature_extraction.sample_to_features_label(sample))
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
