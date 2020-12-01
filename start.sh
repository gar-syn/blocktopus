#!/bin/sh

echo "Starting Blocktopus"

if [ ! -d "/app/data/experiments" ]
then
    python /src/octopus/tools/initialise.py
fi

twistd --nodaemon --pidfile=octopus.pid --logfile octopus.log octopus-editor