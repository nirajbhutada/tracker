#!/bin/bash
set -e
LOGFILE=/home/vijay/Work/DefectTracker/logs/guni.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=3
# user/group to run as
USER= vijay
GROUP= vijay
ADDRESS=127.0.0.1:8000
cd /home/vijay/Work/DefectTracker
#source /home/vijay/myenv27_14/bin/activate
test -d $LOGDIR || mkdir -p $LOGDIR
exec gunicorn_django -w $NUM_WORKERS --bind=$ADDRESS \
  --user=$USER --group=$GROUP --log-level=debug \
    --log-file=$LOGFILE 2>>$LOGFILE
