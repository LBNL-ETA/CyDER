CyDER - Worker
=======

How to use
----

Require python, and all other cosimulation requierments (as Cympy, CYMDIST, etc...)  
If you don't have access to the cosimulation requirements and the CYMDIST models an just test the web interface, consider using the dummy worker (cf. /front_end/dummy_worker/README.md). 

If it's the first time you use the project, run `install.bat` (it will install celery)  
In sym_worker/celery.py set the ip address of the redis db to the ip address of the pc that run the containers

Then run `start_worker.bat` to start the worker


Celery on Windows
-------

Celery dropped the support for Windows since version 4. That's why Celery 3.1.25 is used here as the last version to officially support windows

Cympy and Celery
-----

Cympy can only be imported in one process at a time.  
To be able to use it in a celery worker, the number of process (see Concurrency: http://docs.celeryproject.org/en/3.1/userguide/workers.html#concurrency) must be set to one.  
Moreover celery parse the file sim_worker/tasks.py when starting so the import of cympy can not occur directly at the beginning of file but must be inside a task.  
Finally at the end of each task using using cympy, the worker is killed (`exit(0)`) to 'free' cympy. This raises a celery error and force the creation of a new worker process by celery. 
