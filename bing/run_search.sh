#!/bin/bash

PROGRAM_NAME="/data/apps/sea_growth/src/sea_bing/main.py"

pids=$(ps aux | grep "${PROGRAM_NAME}" | grep -v grep | awk '{print $2}')
if [ -z "$pids" ]; then
    echo "No ${PROGRAM_NAME} running"
    nohup python /data/apps/sea_growth/src/sea_bing/main.py > /data/apps/sea_growth/src/sea_bing/satu.txt &
else
    echo "Program ${PROGRAM_NAME} still running"
fi
