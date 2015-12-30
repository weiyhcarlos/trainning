#!/usr/bin/bash
cd /var/www/data_interface
service nginx start
celery worker -A web.celery --loglevel=DEBUG  -f /var/tmp/celery.log &
uwsgi -i data_interface.ini 

