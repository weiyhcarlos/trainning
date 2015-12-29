#!/usr/bin/bash
celery worker -A web.celery --loglevel=DEBUG &
python web.py &
