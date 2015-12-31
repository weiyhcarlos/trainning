#-*- coding: UTF-8 -*-

import os

from application import app
from application.config import config

config = config[os.getenv('FLASK_CONFIG') or 'default']

if __name__ == "__main__":
    app.run(host=config.APP_HOST, port=config.APP_PORT,
            debug=config.DEBUG)
