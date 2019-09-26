""" genskew.web configuration """

import os

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SERVER_SIDE_SESSION_STORE = 'FS'  # None (client-side), FS (Filesystem), REDIS (Memory)
    FS_SESSION_PATH = base_dir  # Path for session files (in case of store equals 'FS')
