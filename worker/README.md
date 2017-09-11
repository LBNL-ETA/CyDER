CyDER - Worker
=======

How to use
----

Require python

If it's the fisrt time youy use the project, run `install.bat` (it will install celery)  
In sym_worker/celery.py change the address of the redis db to the address of the pc that run the containers

Then run `start_worker.bat` to start the worker

Cympy and Celery
-----

Cympy can only be imported in one process at a time.
To be able to use it in a celery worker, the number of process (see Concurrency: http://docs.celeryproject.org/en/3.1/userguide/workers.html#concurrency) must be set to one.  
Moreover celery parse the file sim_worker/task.py when starting so the import of cympy can not occur in the file directely but inside a task.
