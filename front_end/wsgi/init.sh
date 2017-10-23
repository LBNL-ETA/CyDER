#!/bin/sh

cd /usr/src/app

echo "" > /var/log/cyder/celery_worker.log
echo "" > /var/log/cyder/celery_beat.log
rm celerybeat.pid

supervisord -c /etc/supervisor/supervisord.conf

supervisorctl start celery_worker &&
supervisorctl start celery_beat &&
gunicorn --reload config.wsgi -b 0.0.0.0:8000
