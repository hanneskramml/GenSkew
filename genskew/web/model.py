import uuid
from datetime import datetime
from genskew.config import Config


class Tab(object):
    def __init__(self, title=None) -> None:
        self.id = 'tab_' + uuid.uuid1().__str__()
        self.title = title
        self.timestamp = datetime.now().isoformat()
        self.windowssize = Config.DEFAULT_WINDOWSIZE
        self.stepsize = Config.DEFAULT_STEPSIZE
        self.sequences = {}
