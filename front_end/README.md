CyDER - Front end
======

Containers
-------

- http: run nginx, entry point of the project
- wsgi: run Django the project accessible through gunicorn, use celery to send task to worker
- redis: run redis used as broker for celery
- db: run the db postgres (called cyder_django) used by the Django project

How to use
-------

Require docker and docker-compose (and root privilege to be able to use docker)

If it's the first time you use the project, run `sudo ./install.sh` (it will create database, collect the static files...)
In django-project/sim_worker/celery.py change the address of the redis db to the address of the pc that run the containers  

Then start containers using `sudo docker-compose up`  

Use `sudo docker-compose exec wsgi bash` to open a terminal in the run commands in the Django project.
