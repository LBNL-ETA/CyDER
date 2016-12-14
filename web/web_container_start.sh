#!/bin/bash
# Export variables
export PYTHONPATH=$PYTHONPATH:/usr/src/app/docker_django/
export PYTHONPATH=$PYTHONPATH:/usr/src/app/docker_django/apps/cyder/

# Launch the supervisorctl processes
rm celerybeat.pid
sudo supervisord -n -c /etc/supervisor/supervisord.conf
sudo supervisorctl -c /etc/supervisor/supervisord.conf
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart web_framework
sudo supervisorctl restart celery_beat
sudo supervisorctl restart celery_worker
