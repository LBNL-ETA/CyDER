CyDER - Django project
======

Folders
--------

- config: the Django project config (settings, wsgi.py, urls.py...)  
- sim_worker: the celery module which allow sending task to the simulation worker  
- celery_beat: the celery module used to schedule and run tasks in the wsgi container (in the wsgi container supervisor is used to manage the beat process and the worker process for this module)  
- cyder: the Django apps
- tools: Django python module (python module which need to be used in a Django environment) containing tool functions

Files
------

- manage.py: the Django script to manage the project
- tools.py: a script to perform admin action on CyDER as import new models from the simulation worker (it make use of the tools python/Django module)

-------

All the following commands should be run inside the wsgi container using for example `sudo docker-compose exec wsgi bash` to open a terminal or `sudo docker-compose exec wsgi [your commands]`

Update Django models
------

When the db models of a Django app are modified, a migration is needed.  

To perform it (for exemple on the models app), run
```
python manage.py makemigrations models
python manage.py migrate`
```

Update static files
--------

Static files are originally in the static folder of the django app. To be served by nginx they have to be collected in /var/www on the http container. This location is common to the http and wsgi containers (cf docker-compose.yml).

To collect static files, run
```
python manage.py collectstatic --clear
```

Use the Django debug server
-------

You can start the debug server by running `python manage.py runserver 0.0.0.0:8080`. You can the access it at http://127.0.0.1:8080/  
This can be useful when working on static files (to prevent running collectstatic all the time)

Import/Update CYME models into the Postgres DB
-------

Run
```
python tools.py import_models [models_names]
```
`models_names` being the list of the names of the models (for example `"BU0001" "AT" "OC0001"`)
