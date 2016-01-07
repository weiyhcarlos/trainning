#!/bin/bash
if [ $# != 2 ]; then
    echo "USAGE::$0 code_path num(num of celery)"
    exit
fi
i=1

for i in `seq $2` 
do
  docker run --link rabbitmq1:rabbit -v $1:/tasks --name celery$i -d  celery  celery worker -A tasks --workdir=/tasks &
done
