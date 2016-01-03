#!/bin/bash
ids=`docker ps -a|  grep celery |awk '{print $1}'`
docker stop $ids
docker rm $ids
