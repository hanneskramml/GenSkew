import traceback
from Bio import SeqIO
from genskew import log


class SeqLoader:

    class Sequence:
        def __init__(self, id) -> None:
            self.id = id
            self.name = None
            self.desc = None
            self.len = 0
            self.alphabet = None
            self.data = ''

    @classmethod
    def parse(cls, file):
        seqs = []

        try:
            for record in SeqIO.parse(file, 'fasta'):
                seq = cls.Sequence(record.id)
                seq.name = record.name
                seq.desc = record.description
                seq.len = len(record.seq)
                seq.alphabet = str(record.seq.alphabet)
                seq.data = str(record.seq)

                seqs.append(seq)

        except Exception:
            log.error(traceback.format_exc(0))
            return []

        log.debug("%i sequence record(s) loaded", len(seqs))
        return seqs

