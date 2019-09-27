import uuid
from datetime import datetime as dt
from genskew.lib import GenSkew as gs


class Tab(object):
    def __init__(self, title=None) -> None:
        self.id = 'tab_' + uuid.uuid1().__str__()
        self.title = title
        self.timestamp = dt.now().strftime("%Y-%m-%d %H:%M")
        self.sequences = []
        self.settings = None
        self.plot = None


class Settings(object):
    def __init__(self, seqlen) -> None:
        self.n1 = gs.DEFAULT_N1
        self.n2 = gs.DEFAULT_N2
        self.windowsize = int(seqlen / gs.DEFAULT_WINDOWSIZE)
        self.stepsize = int(seqlen / gs.DEFAULT_STEPSIZE)


class Sequence:
    def __init__(self, id) -> None:
        self.id = id
        self.name = None
        self.desc = None
        self.enabled = True
        self.len = 0
        self.alphabet = None
        self.data = ''


class PlotData(object):
    def __init__(self) -> None:
        self.total_len = 0
        self.gc_content = 0
        self.contig_start_pos = []
        self.x_seq_position = []
        self.y_skew_normal = []
        self.y_skew_cumulative = []

    def get_plot_data(self):
        skew_normal = []
        skew_cumulative = []

        for i in range(0, len(self.x_seq_position)):
            skew_normal.append({'x': self.x_seq_position[i], 'y': round(self.y_skew_normal[i], 3)})
            skew_cumulative.append({'x': self.x_seq_position[i], 'y': round(self.y_skew_cumulative[i], 3)})

        return {'origin': self.get_pos_for_origin(), 'separator_pos': self.contig_start_pos,
                'skew_normal': skew_normal, 'skew_cumulative': skew_cumulative}

    def get_pos_for_origin(self):
        return self.x_seq_position[self.y_skew_cumulative.index(min(self.y_skew_cumulative))]
