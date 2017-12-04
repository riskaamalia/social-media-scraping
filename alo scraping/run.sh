#!/bin/bash

PROGRAM_NAME="/data/apps/sea_growth/src/sea_alodokter/main.py"

pids=$(ps aux | grep "${PROGRAM_NAME}" | grep -v grep | awk '{print $2}')
if [ -z "$pids" ]; then
    echo "No ${PROGRAM_NAME} running"
    nohup python /data/apps/sea_growth/src/sea_alodokter/main.py > /data/apps/sea_growth/src/sea_alodokter/out.txt &
else
    echo "Program ${PROGRAM_NAME} still running"
fi
