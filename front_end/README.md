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

If it's the first time you use the project, run `sudo ./install.sh` (it will create database, collect the static files for nginx, ask to create the Django superuser...).

Then start containers using `sudo docker-compose up`  

Now you should install and start the worker (cf /woker/README.md) or the dummy worker (cf /dummy_worker/README.md) and import models into the front end DB (cf /front_end/django_project/README.md)
