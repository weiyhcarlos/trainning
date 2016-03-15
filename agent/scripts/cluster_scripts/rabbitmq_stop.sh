#!/bin/bash
ids=`docker ps -a|  grep rabbitmq |awk '{print $1}'`
docker stop $ids
docker rm $ids
dns=`docker ps -a | grep docker-dns | awk '{ print $1}'`
docker stop $dns
docker rm $dns
