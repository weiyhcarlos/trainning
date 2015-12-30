#!/usr/bin/bash
cd /var/www/data_interface
celery worker -A web.celery --loglevel=DEBUG  -f /var/tmp/celery.log &
python web.py &
