def make_vocab():
    vocab_samples = 10000
    strlen = 5
    vset = set()
    for i in range(vocab_samples):
        vset.add(''.join(random.choices(string.ascii_uppercase + string.digits, k=strlen)))
    vocab = {i: random.random() for i in vset}
    return vocab