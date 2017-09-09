CyDER - Front end
======

Containers
-------

- http: run nginx, entry point of the project
- wsgi: run django accesible throught gunicorn, use celery to send task to worker
- redis: run redis used as broker for celery
- db: run the db postgres (called cyder_django)
 used by the django project

Django project
--------

- CyDER: the django main project  
- sym_worker: the celery module wich allow sending task to the worker  
- testapp: the django app (http://127.0.0.1/testapp/)
- tools: django module containg tool script

How to use
-------

Require docker and docker-compose (and root priviledge to be able to use docker)

If it's the fisrt time youy use the project, run `sudo ./install.sh` (it will create database, collect the static files...)  
In django-project/CyDER/setting.py, in ALLOWED_HOST, change the address to the address of the pc that run the containers  
In django-project/sym_worker/celery.py change the address of the redis db to the address of the pc that run the containers  

Then start containers using `sudo docker-compose up`
