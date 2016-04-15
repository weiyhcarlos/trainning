#!/usr/bin/bash
cd /var/www/data_interface
service nginx start
export PYTHONPATH=conf:./:./code
celery worker -A code.celery_worker.celery --loglevel=DEBUG  -f /var/tmp/celery.log &
uwsgi -i data_interface.ini

