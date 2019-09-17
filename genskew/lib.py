from genskew import log
from genskew.input import SeqLoader
from genskew.utils import compute_skew_data
from genskew.config import Config


class GenSkew:

    @staticmethod
    def plot(seqfile, n1=Config.DEFAULT_N1, n2=Config.DEFAULT_N2, window=Config.DEFAULT_WINDOWSIZE,
             step=Config.DEFAULT_STEPSIZE, output='plot.png'):

        skew_data = {}
        for seq in SeqLoader.parse(seqfile):
            skew_data[seq.id] = compute_skew_data(seq.data, n1, n2, window, step)

        log.debug(skew_data)
