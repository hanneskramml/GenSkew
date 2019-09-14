

def compute_skew_data(seq, n1, n2, window, step):
    values = []

    for i in range(0, len(seq), step):
        section = seq[i: i+window]
        n_n1 = section.count(n1)
        n_n2 = section.count(n2)

        try:
            skew = (n_n1 - n_n2) / (n_n1 + n_n2)
        except ZeroDivisionError:
            skew = 0.0

        values.append(skew)
    return values

