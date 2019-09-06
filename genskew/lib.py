from genskew import log
from genskew.input import SeqFile
from genskew.utils import nucleotide_skew


def create_plot(filepath, n1='G', n2='C', window=1000, step=1000):
    file = SeqFile(filepath)
    file.open()
    seq = file.parse_sequence()

    nucleotide_skew(seq, n1, n2, window, step)
