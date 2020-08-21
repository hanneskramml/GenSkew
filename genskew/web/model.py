import json
from uuid import uuid1
from Bio import SeqRecord
from datetime import datetime as dt
from genskew.lib import GenSkew


class SeqFile(object):
    def __init__(self, title=None) -> None:
        self.id = 'file_' + uuid1().__str__()
        self.title = title
        self.timestamp = dt.now().strftime("%Y-%m-%d %H:%M")
        self.seqs = []
        self.plot = None


class SeqRec(SeqRecord.SeqRecord):

    def __new__(cls, *args, **kwargs):
        return object.__new__(SeqRec)

    def __init__(self, seq, id="<unknown id>", name="<unknown name>", description="<unknown description>", dbxrefs=None,
                 features=None, annotations=None, letter_annotations=None):
        super().__init__(seq, id, name, description, dbxrefs, features, annotations, letter_annotations)
        self.enabled = True


class ContigPlot(object):
    def __init__(self, seqs) -> None:
        self.seqs = seqs
        self.settings = None
        self.gc_content = 0
        self.x_position = []
        self.y_skew_normal = []
        self.y_skew_cumulative = []

    def get_total_len(self):
        return sum([len(seq) for seq in self.seqs])

    def get_pseudo_contig(self):
        pseudo_contig = [str(seq.seq) for seq in self.seqs]
        return ''.join(pseudo_contig)

    def get_start_pos(self):
        contig_start_pos = []

        for i in range(0, len(self.seqs)):
            if i == 0:
                contig_start_pos.append(1)
            else:
                contig_start_pos.append(contig_start_pos[i-1] + len(self.seqs[i-1]))

        return contig_start_pos

    def get_origin(self):
        return self.x_position[self.y_skew_cumulative.index(min(self.y_skew_cumulative))]

    def get_terminus(self):
        return self.x_position[self.y_skew_cumulative.index(max(self.y_skew_cumulative))]

    def get_plot_data(self):
        skew_normal = []
        skew_cumulative = []

        for i in range(0, len(self.x_position)):
            skew_normal.append({'x': self.x_position[i], 'y': round(self.y_skew_normal[i], 3)})
            skew_cumulative.append({'x': self.x_position[i], 'y': round(self.y_skew_cumulative[i], 3)})

        return json.dumps({'skew_normal': skew_normal, 'skew_cumulative': skew_cumulative,
                           'separator_pos': self.get_start_pos()[1:], 'origin': self.get_origin(), 'terminus': self.get_terminus()})


class Settings(object):
    def __init__(self, plot) -> None:
        self.plot = plot
        self.n1 = GenSkew.DEFAULT_N1
        self.n2 = GenSkew.DEFAULT_N2
        self.windowsize = 0
        self.stepsize = 0
        self.set_default_size()

    def set_default_size(self):
        contig_len = self.plot.get_total_len()
        self.windowsize = int(contig_len / GenSkew.DEFAULT_WINDOWSIZE)
        self.stepsize = int(contig_len / GenSkew.DEFAULT_STEPSIZE)

    def reset_all(self):
        self.n1 = GenSkew.DEFAULT_N1
        self.n2 = GenSkew.DEFAULT_N2
        self.set_default_size()
