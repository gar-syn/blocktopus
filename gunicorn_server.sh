#!/bin/sh
gunicorn --bind 0.0.0.0:8003 --worker-tmp-dir /dev/shm --workers 4 wsgi:app