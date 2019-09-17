import uuid
from datetime import datetime as dt
from genskew.config import Config


class Tab(object):
    def __init__(self, title=None) -> None:
        self.id = 'tab_' + uuid.uuid1().__str__()
        self.title = title
        self.timestamp = dt.now().strftime("%Y-%m-%d %H:%M")
        self.settings = None
        self.sequences = {}


class Settings(object):
    def __init__(self) -> None:
        self.n1 = Config.DEFAULT_N1
        self.n2 = Config.DEFAULT_N2
        self.windowsize = Config.DEFAULT_WINDOWSIZE
        self.stepsize = Config.DEFAULT_STEPSIZE
