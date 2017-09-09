CyDER Test MHebant
=======

Objective
------

Make an architecture in docker containers to run nginx, django, gunicorn, celery, redis and postgresql.
Make them working together.  
Create a Django app (called testapp) to run a task on a celery worker.  

Project components
-----

- front_end: Front web django project with databases and nginx...
- worker: The Windows worker that handle simulations

Celery on Windows
-------

Celery dropped the support for Windows since version 4. That's why Celery 3.1.25 is used here as the last version to officialy support windows
