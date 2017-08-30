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
worker: run the celery worker

Sources (in CyDER folder)
--------

CyDER: the django main project
celery_test: the celery project
testapp: the django app that "call" the worker using celery (http://127.0.0.1/testapp/)
