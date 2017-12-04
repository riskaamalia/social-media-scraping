#!/bin/bash

PROGRAM_NAME="/data/apps/sea_growth/src/sea_google_search/main.py 2,1,1"

pids=$(ps aux | grep "${PROGRAM_NAME}" | grep -v grep | awk '{print $2}')
if [ -z "$pids" ]; then
    echo "No ${PROGRAM_NAME} running"
    nohup python /data/apps/sea_growth/src/sea_google_search/main.py 2,1,1 > /data/apps/sea_growth/src/sea_google_search/dua.txt &
else
    echo "Program ${PROGRAM_NAME} still running"
fi

PROGRAM_NAME="/data/apps/sea_growth/src/sea_google_search/main_without_driver.py"

pids=$(ps aux | grep "${PROGRAM_NAME}" | grep -v grep | awk '{print $2}')
if [ -z "$pids" ]; then
    echo "No ${PROGRAM_NAME} running"
    nohup python /data/apps/sea_growth/src/sea_google_search/main_without_driver.py > /data/apps/sea_growth/src/sea_google_search/tiga.txt &
else
    echo "Program ${PROGRAM_NAME} still running"
fi
