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
        features.add(prefix + '_window_%d_lemma_%s' % (i, token.lemma))
        word = sample.sentence.text[token.start_offset:token.end_offset].lower()
        features.add(prefix + '_window_%d_word_%s' % (i, word))
    # window after
    for i in range(1, 3):
        idx = max(indices) + i
        if idx not in range(len(sample.sentence.tokens)):
            continue
        features.add(prefix + '_window_%d_lemma_%s' % (i, token.lemma))
        word = sample.sentence.text[token.start_offset:token.end_offset].lower()
        features.add(prefix + '_window_%d_word_%s' % (i, word))
    return features

def sample_to_features(sample):
    features = set()
    # bag-of-words features
    features = features.union(sentence_bag_of_words_features(sample))

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

def sample_to_features_label(sample):
    return (sample_to_features(sample), sample.positive)
