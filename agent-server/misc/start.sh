#!/usr/bin/bash
cd /var/www/api_backend
service nginx start
uwsgi -i api_backend.ini 