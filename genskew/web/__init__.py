"""GenSkew: WebGUI Package"""

import logging
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_kvsession import KVSessionExtension
from simplekv.fs import FilesystemStore
from genskew.config import Config

log = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)

if Config.SERVER_SIDE_SESSION_STORE == 'FS':
    store = FilesystemStore(Config.SERVER_SIDE_SESSION_PATH)
    KVSessionExtension(store, app)

from genskew.web import controller
