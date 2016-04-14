#!/bin/bash
apt-get install python-pip
pip install ntplib
pip install pyyaml
pip install pymongo
pip install psutil
if [ ! -e /etc/init.d/agent ];then
    cp ./agent /etc/init.d/
fi
if [ ! -d /var/agent ];then
    mkdir /var/agent
    cp -ar ../../code/agent/*  /var/agent
fi
 

