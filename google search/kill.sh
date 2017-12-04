#!/bin/sh

PROGRAM_NAME=google_search

PID=$(ps -ef | egrep ".*python.*${PROGRAM_NAME}" | grep -v grep | awk '{print $2}')
if [ "$PID" = "" ]; then
        echo "${PROGRAM_NAME} is not running."
else
        echo "Stopping ${PROGRAM_NAME}..."
        kill ${PID}
        while [ -e /proc/$PID ]
        do
           sleep 1
        done
        echo "${PROGRAM_NAME}(${PID}) stopped."
fi