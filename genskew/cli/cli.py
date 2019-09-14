import argparse
from genskew.cli import log
from genskew.lib import GenSkew


def main():

    parser = argparse.ArgumentParser(prog="genskew", description="GenSkew: Genomic nucleotide skew application")
    parser.add_argument('SeqFile', type=str, help='Sequence input file (RAW, FASTA)')
    parser.add_argument('-o', '--output', type=str, help='Filename for generated plot image (Default: plot.png)',
                        default='plot.png')
    args = parser.parse_args()
    log.info(args)
