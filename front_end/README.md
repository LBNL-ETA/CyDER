CyDER - Front end
======

Containers
-------

- http: run nginx, serve static files, redirect dynamic request on wsgi container
- wsgi: run the Django project, accessible through gunicorn, use celery to send task to worker
- redis: run redis used as broker for celery
- db: run the postgres db (called cyder_django) used by the Django project

How to use
-------

Require docker and docker-compose (and root privilege to be able to use docker)

If it's the first time you use the project, run `sudo ./install.sh` (it will create database, collect the static files for nginx...). In django-project/sim_worker/celery.py change the address of the redis db to the address of the pc that run the containers  

Then start containers using `sudo docker-compose up`  
