#!/bin/bash

PROGRAM_NAME="MainUsingSelenium.py"

pids=$(ps aux | grep "${PROGRAM_NAME}" | grep -v grep | awk '{print $2}')
if [ -z "$pids" ]; then
    echo "No ${PROGRAM_NAME} running"
    nohup python /data/apps/sea_growth/src/sea_facebook/src/MainUsingSelenium.py > /dev/null 2>&1 &
else
    echo "Program ${PROGRAM_NAME} still running"
fi

