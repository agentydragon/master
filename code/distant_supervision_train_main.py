#!/usr/bin/python3

import nltk
import argparse
import random
import file_util
import training_samples_pb2

def sample_to_features_label(sample):
    """Bag of words features."""
    features = {}
    for token in sample.sentence.tokens:
        features[token.lemma.lower()] = 1
    return (features, 1 if sample.positive else 0)

def samples_to_features_labels(samples):
    return [sample_to_features_label(sample) for sample in samples]

def main():
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('--training_data', required=True)
    args = parser.parse_args()

    print("Loading training data...")
    training_data = file_util.parse_proto_file(
        training_samples_pb2.TrainingSamples,
        args.training_data)

    for relation_training_samples in training_data.relation_samples:
        relation = relation_training_samples.relation
        print("Training relation:", relation)

        samples = list(relation_training_samples.samples)
        positives = [sample for sample in samples if sample.positive]
        negatives = [sample for sample in samples if not sample.positive]
        print("Positives:", len(positives), "negatives:", len(negatives))
        samples = positives + negatives
        random.shuffle(samples)

        split = round(0.5 * len(samples))
        train = samples[:split]
        test = samples[split:]

        print(len(train), "train samples, positive:",
              len([x for x in train if x.positive]))
        print(len(test), "test samples, positive:",
              len([x for x in test if x.positive]))

        #if relation != 'P26':
        #    continue

        train_features_labels = samples_to_features_labels(train)
        test_features_labels = samples_to_features_labels(test)

        classifier = nltk.NaiveBayesClassifier.train(train_features_labels)
        print('Accuracy:', nltk.classify.accuracy(classifier, test_features_labels))
        classifier.show_most_informative_features(5)
        print()

if __name__ == '__main__':
    main()
