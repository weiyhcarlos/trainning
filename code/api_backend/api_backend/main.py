#-*- coding: UTF-8 -*-

from application import app
from application import config

if __name__ == "__main__":
    app.run(host=config.APP_HOST, port=config.APP_PORT,
            debug=config.DEBUG)
