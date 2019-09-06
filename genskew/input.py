from Bio import SeqIO
from genskew import log


class SeqFile:
    """A class representing the input file for the sequence to be analysed"""

    def __init__(self, filepath):
        self.filepath = filepath
        self.format = None
        self.__file = None

    def open(self):
        self.__file = open(self.filepath)

    def validate_format(self):
        self.format = 'fasta'

    def parse_sequence(self):
        for record in SeqIO.parse(self.__file, self.format):
            log.info("SeqID: %s", record.id)
