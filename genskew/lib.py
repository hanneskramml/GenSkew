""" GenSkew lib: Module for using the app as python library """

from Bio import SeqIO
from matplotlib import pyplot
from genskew import utils


class GenSkew:

    DEFAULT_N1 = 'G'
    DEFAULT_N2 = 'C'
    DEFAULT_WINDOWSIZE = 1000
    DEFAULT_STEPSIZE = 1000

    @classmethod
    def plot(cls, seqfile, n1=DEFAULT_N1, n2=DEFAULT_N2, window=None, step=None):
        """Plot skew data ...tba"""

        seq_recs = [str(seq.seq) for seq in SeqIO.parse(seqfile, 'fasta')]
        pseudo_contig = ''.join(seq_recs)

        separators = []
        for i in range(0, len(seq_recs[1:])):
            if i == 0:
                separators.append(len(seq_recs[i]) + 1)
            else:
                separators.append(separators[i-1] + len(seq_recs[i]) + 1)

        if not window:
            window = int(len(pseudo_contig) / cls.DEFAULT_WINDOWSIZE)
        if not step:
            step = int(len(pseudo_contig) / cls.DEFAULT_STEPSIZE)

        position, skew_normal, skew_cumulative = utils.compute_skew_data(pseudo_contig, n1, n2, window, step)

        fig = pyplot.figure()
        utils.draw_figure(fig, position, skew_normal, skew_cumulative, separators)
        pyplot.show()
