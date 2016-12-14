# Launch the supervisorctl processes
sudo service supervisor start
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart web_framework
sudo supervisorctl restart celery_beat
sudo supervisorctl status
