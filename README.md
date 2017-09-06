CyDER Test MHebant
=======

Objective
------

Make an architecture in docker containers to run nginx, django, gunicorn, celery, redis (and later postgresql).  
Make them working together.  
Create a Django app (called testapp) to run a task on a celery worker (called celery_test).  

Containers
-------

http: run nginx, entry point of the project  
wsgi: run django accesible throught gunicorn, use celery to send task to worker  
redis: run redis serving as broker for celery  
(worker: run the celery worker) => Now on a separate PC on Windows

Sources (in CyDER folder)
--------

CyDER: the django main project  
celery_test: the celery project  
testapp: the django app that "call" the worker using celery (http://127.0.0.1/testapp/)

Celery on Windows
-------

Celery dropped the support for Windows since version 4. That's why Celery 3.1.25 is used here as the last version to officialy support windows

How to use
---------

Container PC: have docker and docker-compose installed  
WorkerPC: have python installed

- In CyDER/django/CyDER/setting.py, in ALLOWED_HOST, change the address to the address of the pc that run the containers  
- In CyDER/django/celery_test/celery.py change the address of the redis db to the address of the pc that run the containers  
- Copy the repo on the PC wich will run the containers and type `docker-compose up`
- On the Windows PC wich will run the worker type `pip install celery[redis]==3.1.25` to install Celery
- Copy the repo on the Windows PC wich will run the worker and type './start_worker_on_win.bat'  
