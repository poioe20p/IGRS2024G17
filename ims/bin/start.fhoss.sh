#!/bin/bash

export JAVA_HOME=/usr/
DIR=`pwd`

cd /opt/OpenIMSCore/FHoSS/deploy
screen -S FHoSS -d -m -h 10000 ./startup.sh
#./startup.sh

cd $DIR
