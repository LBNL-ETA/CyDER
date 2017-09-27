CyDER - Django project
======

Project folders
--------

- config: the Django project config (settings, wsgi.py, urls.py...)  
- sim_worker: the celery module which allow sending task to the worker  
- cyder: the Django apps
- tools: Django module containing tool script

-------

The following commands should be run inside the wsgi container using for example `sudo docker-compose exec wsgi bash` to open a terminal or `sudo docker-compose exec wsgi [your commands]`

Update Django models
------

Run
```
python manage.py makemigrations grid_models
python manage.py migrate`
```

Update static files
--------

Run
```
python manage.py collectstatic --clear
```

Use the Django debug server
-------

You can start the debug server by typing `python manage.py runserver 0.0.0.0:8080`. You can the access it by http://127.0.0.1:8080/  
This can be useful when working on static files (to prevent running collectstatic all the time)

-------

The following commands should be run inside the Django context, using the shell `sudo docker-compose exec wsgi python manage.py shell` or exporting the Django setting file of the project.

Import/Update CYME models indo the postgres DB
-------

Run
```
import tools.db_models
tools.db_models.import_model(modelfile)
```
`modelfile` being the name of the file of the model (for example `BU0001.sxst`)
