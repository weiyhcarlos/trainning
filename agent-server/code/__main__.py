#!/usr/bin/env python
# -*- encoding=utf8 -*-
'''
Filename: __main__.py
'''

import os

from code import app
from conf.config import config

config = config[os.getenv('FLASK_CONFIG') or 'default']

if __name__ == "__main__":
    app.run(host=config.APP_HOST, port=config.APP_PORT,
            # debug=config.DEBUG
           )
