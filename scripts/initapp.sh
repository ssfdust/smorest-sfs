#!/bin/sh
wait-for-it -t 300 db:5432 -- echo "Database is ready"
wait-for-it -t 300 redis:6379 -- echo "Redis is ready"
wait-for-it -t 300 rabbitmq:5432 -- echo "Rabbitmq is ready"
if [ "$APP" = "web" ];then
    flask db upgrade
    gunicorn -k "egg:meinheld#gunicorn_worker" -c gunicorn.py smorest_sfs.app:app
elif [ "$APP" = "celery" ];then
    celery --app=smorest_sfs.app:celery_app worker -l INFO -E
elif [ "$APP" = "beat" ];then
    celery beat --app=smorest_sfs.app:celery_app -S redbeat.RedBeatScheduler --pidfile=
fi
