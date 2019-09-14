import os

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEFAULT_WINDOWSIZE = 1000
    DEFAULT_STEPSIZE = 1000

    ### genskew.web configuration ###
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SERVER_SIDE_SESSION_STORE = 'FS'  # None (client-side), FS (Filesystem), REDIS (Memory)
    SERVER_SIDE_SESSION_PATH = base_dir  # Path for session files (in case of store equals 'FS')
