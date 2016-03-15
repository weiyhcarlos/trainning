# -*- coding: utf-8 -*-

import os
from app import celery, create_app
from app import upload_task

#使用app的配置重新配置celery
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
#压入flask application context
#celery中可以使用current_app获取到当前app对象
# app.app_context().push()
