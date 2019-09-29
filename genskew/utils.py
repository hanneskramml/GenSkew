""" GenSkew utils: Module containing features shared by all packages """


def compute_skew_data(seq, n1, n2, window, step):
    """Compute skew data ...tba"""

    position = []
    skew_normal = []
    skew_cumulative = []

    for i in range(0, len(seq), step):
        section = seq[i: i + window]
        n_n1 = section.count(n1)
        n_n2 = section.count(n2)

        try:
            skew = (n_n1 - n_n2) / (n_n1 + n_n2)
        except ZeroDivisionError:
            skew = 0.0

        position.append(i + 1)
        skew_normal.append(skew)
        if i == 0:
            skew_cumulative.append(skew)
        else:
            skew_cumulative.append(skew + skew_cumulative[-1])

    return position, skew_normal, skew_cumulative


def compute_gc_content(seq):
    """Compute GC nucleotide content for a given (pseudo-)contig"""

    n_gc = sum(seq.count(x) for x in ['G', 'g', 'C', 'c'])

    try:
        content = n_gc * 100.0 / len(seq)
    except ZeroDivisionError:
        content = 0.0

    return content


def draw_figure(fig, x_seq_position, y_skew_normal, y_skew_cumulative, x_contig_separators):
    """Create/draw matplotlib figure ...tba"""

    plt1 = fig.add_subplot(2, 1, 1)

    plt1.plot(x_seq_position, y_skew_normal, label='normal', color='tab:blue')
    plt1.xaxis.set_ticklabels([])
    plt1.grid()
    plt1.legend()

    plt2 = fig.add_subplot(2, 1, 2)
    plt2.plot(x_seq_position, y_skew_cumulative, label='cumulative', color='tab:orange')
    plt2.grid()
    plt2.legend()

    for pos in x_contig_separators:
        plt1.axvline(x=pos, color='tab:brown', linestyle=':')
        plt2.axvline(x=pos, color='tab:brown', linestyle=':')

    i_min = y_skew_cumulative.index(min(y_skew_cumulative))
    plt1.axvline(x=x_seq_position[i_min], color='tab:red', linestyle='-')
    plt2.axvline(x=x_seq_position[i_min], color='tab:red', linestyle='-')
