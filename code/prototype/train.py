from prototype.lib import sample_repo

mother = 'P25'
father = 'P22'
brother = 'P7'
child = 'P40'
spouse = 'P26'

samples = sample_repo.load_samples(mother)

for sample in samples:
    lemmas = []
    for token in sample.sentence.tokens:
        lemmas.append(token.lemma)
    print(" ".join(lemmas))
