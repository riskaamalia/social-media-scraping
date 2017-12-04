#!/bin/bash

PROGRAM_NAME="/data/apps/sea_growth/src/sea_twitter/main.py"

pids=$(ps aux | grep "${PROGRAM_NAME}" | grep -v grep | awk '{print $2}')
if [ -z "$pids" ]; then
    echo "No ${PROGRAM_NAME} running"
    nohup /opt/python27/bin/python /data/apps/sea_growth/src/sea_twitter/main.py > /data/apps/sea_growth/src/sea_twitter/satu.txt &
else
    echo "Program ${PROGRAM_NAME} still running"
    echo "Stopping ${PROGRAM_NAME}..."
        kill ${pids}
        while [ -e /proc/$pids ]
        do
           sleep 1
        done
        echo "${PROGRAM_NAME}(${pids}) stopped."

        echo "Start ${PROGRAM_NAME} running"
        nohup /opt/python27/bin/python /data/apps/sea_growth/src/sea_twitter/main.py > /data/apps/sea_growth/src/sea_twitter/satu.txt &

fi
