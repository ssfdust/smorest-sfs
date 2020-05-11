#!/bin/sh
if [ "$APP" = "web" ];then
    waitfor -t 300 db:5432 redis:6379 rabbitmq:5672 -- flask db upgrade
    gunicorn -k "egg:meinheld#gunicorn_worker" -c gunicorn.py smorest_sfs.app:app
elif [ "$APP" = "celery" ];then
    waitfor -t 300 db:5432 redis:6379 rabbitmq:5672 -- celery --app=smorest_sfs.app:celery_app worker -l INFO -E
elif [ "$APP" = "beat" ];then
    waitfor -t 300 db:5432 redis:6379 rabbitmq:5672 -- celery beat --app=smorest_sfs.app:celery_app -S redbeat.RedBeatScheduler
fi
