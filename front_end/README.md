CyDER - Front end
=================

Containers
----------

Docker containers which support the web interface

- http: run nginx, serve static files, redirect dynamic request on wsgi container
- wsgi: run the Django project, accessible through gunicorn, use celery to send task to worker
- redis: run redis used as broker for celery
- db: run the postgres db (called cyder_django) used by the Django project

Workers:
--------

A worker is an application which execute the simulation for the web interface and from which the web interfece can have access to data from the simulation models.
It's linked to the web interface throught Celery.

- worker: this worker must run on Windows and require the CymPy, CIME and the models from PG&E to work.
- dummy_worker: a Docker container running a worker which outputs random values. Usefull for testing when you cannot use the true worker.


How to use
----------

Requires docker and docker-compose (and root privilege to be able to use docker)

If it's the first time you use the project, run `sudo ./install.sh` (it will create a database, collect the static files for nginx, ask to create the Django superuser...).

Then start containers using `sudo docker-compose up`  
Then run the Django develoment server using `sudo docker-compose exec wsgi python manage.py runer 0.0.0.0:8080`

The web site is now accessible at https://127.0.0.1/  
The web site use modern javascript (incompatible with IE) and requires an up-to-date browser (Chrome or Firefox are recommended, but it should work fine in Opera, Safari, Edge...). In the current version of Firefox (58.0), the new JS modules (used in the project) are still under the flag `dom.moduleScripts.enabled`. You will have to enable it in `about:config` otherwise the web site won't work.  
Skip the security warning. It appear because Nginx use a self-signed certificate for ssl.

Now you should install and start the worker (cf wroker/README.md) or the dummy worker (cf dummy_worker/README.md) and import models into the front end DB (cf django_project/README.md)