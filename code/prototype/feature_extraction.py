def sample_to_features(sample):
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

    # window before subject
    for i in range(-2, 0):
        idx = min(sample.subject_token_indices) - i
        if idx not in range(len(sample.sentence.tokens)):
            continue
        features.add('subject_window_%d_lemma_%s' % (i, token.lemma))
        word = sample.sentence.text[token.start_offset:token.end_offset].lower()
        features.add('subject_window_%d_word_%s' % (i, word))

    # window before object
    for i in range(-2, 0):
        idx = min(sample.object_token_indices) - i
        if idx not in range(len(sample.sentence.tokens)):
            continue
        features.add('object_window_%d_lemma_%s' % (i, token.lemma))
        word = sample.sentence.text[token.start_offset:token.end_offset].lower()
        features.add('object_window_%d_word_%s' % (i, word))

    # window after subject
    for i in range(1, 3):
        idx = max(sample.subject_token_indices) + i
        if idx not in range(len(sample.sentence.tokens)):
            continue
        features.add('subject_window_%d_lemma_%s' % (i, token.lemma))
        word = sample.sentence.text[token.start_offset:token.end_offset].lower()
        features.add('subject_window_%d_word_%s' % (i, word))

    # window after object
    for i in range(1, 3):
        idx = max(sample.object_token_indices) + i
        if idx not in range(len(sample.sentence.tokens)):
            continue
        features.add('object_window_%d_lemma_%s' % (i, token.lemma))
        word = sample.sentence.text[token.start_offset:token.end_offset].lower()
        features.add('object_window_%d_word_%s' % (i, word))

    if min(sample.subject_token_indices) < min(sample.object_token_indices):
        features.add('subject_first')
    else:
        features.add('object_first')
    return features

def sample_to_features_label(sample):
    return (sample_to_features(sample), sample.positive)
