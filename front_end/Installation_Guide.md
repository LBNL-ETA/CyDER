Installation Guide
==================

* 1- Clone Git repo by running in a terminal window
```sh
git clone https://github.com/LBNL-ETA/CyDER.git
```
* 2- Download and install Docker: https://www.docker.com/get-docker

* 3- Start Docker

The following commands and scripts are to be run from a terminal window at the root of your repo.

* 4- Run the ./front_end/install.sh file


* 5- Replace all broker and backend IP adresses with your IP adress in all celery.py files:
	- ./front_end/django-project/sim_worker/celery.py
	- ./front_end/worker/sim_worker/celery.py
	- ./front_end/dummy_worker/sim_worker/celery.py

* 6- Replace broker and backend IP adress with the same IP adress as in '5-' on the worker computer running the simulations:
	- ./front_end/worker/celery.py

* 7- Start the docker containers running the command 
```sh
'docker-compose up'
```
* 8- Start the django development server running the command
```sh	
'docker-compose exec wsgi python manage.py runserver 0.0.0.0:8080'
```
* 9- On the worker computer running the simulations start the worker by executing the file
	- ./front_end/worker/start_worker.bat

* 10-	Import subtsation models to the web interface by running the command
```sh
'docker-compose exec wsgi python tools.py import_models' 
```
followed by the names of the models you want to import. For example:
```sh
'docker-compose exec wsgi python tools.py import_models "BU0006" '
'docker-compose exec wsgi python tools.py import_models "BU0006" "AT0001" "SW0007" '
```

* 11-	Access and use the web interface in your web browser at http://127.0.0.1:8080/ 