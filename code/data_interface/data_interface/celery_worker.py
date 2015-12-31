# -*- coding: utf-8 -*-

import os
from app import celery, create_app
from app import upload_task

#压入flask application context
#celery中可以使用current_app获取到当前app对象

# app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# app.app_context().push()
