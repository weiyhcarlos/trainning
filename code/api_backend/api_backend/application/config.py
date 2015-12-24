#-*- coding: UTF-8 -*-

import os

def env_default(k, default):
    v = os.environ.get(k, default)
    globals()[k] = v

env_default("REDIS_ADDR", 'redis')
env_default("REDIS_PORT", 6379)

env_default("APP_HOST", '0.0.0.0')
env_default("APP_PORT", 8888)

env_default("MONGO_HOST", "123.58.165.133")
env_default("MONGO_PORT", 32774)
env_default("MONGO_DATABASE", "machine_test")

env_default("DEBUG", True)
env_default("CONNECT", False)
