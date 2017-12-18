CyDER - Dummy worker
======

Allow you to test the front end without access to the worker.
It can create random models of different sizes and random results for the configuration and the simulation

How to use
---------

Require docker and docker-compose (and root privilege to be able to use docker)

In sym_worker/celery.py change the address of the redis db to the address of the pc that run the containers for the front end.  
Run `docker-compose up` to start the dummy workers  
If you change the source in sim_worker you will have to rebuild the worker with `docker-compose up --build`

You can then use this worker to import dummy models in the front end using the method describe in /front_end/README.md "Import/Update CYME models into the Postgres DB".  
Use model name `SMALL_DUMMY` to generate a small dummy (about 50 nodes)  
Use model name `BIG_DUMMY` to generate a big model (about 2500 nodes)  
Use model name `HUGE_DUMMY` to generate a huge model (about 6500 nodes)  
Any other name will generate a medium size model (about 500 nodes)

Add the dummy worker to the docker-compose.yml du front end
-----------------

Do this if you just want to run every thing locally.

Add this add the end of /front_end/docker-compose.yml:
```
dummy_worker:
        build: ../dummy_worker
        links:
                - redis
```
And in /dummy_worker/sim_worker/celery.py change the redis IP address with `redis` :
```
broker='redis://redis:6379/0',
backend='redis://redis:6379/0',
```

Then you just have to start the front end containers by running `docker-compose up` in /front_end/ to start every thing
