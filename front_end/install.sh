#!/bin/bash
DONE=0
docker-compose up -d db &&
CMD="RETRIES=5
until psql -h 127.0.0.1 -U postgres -w -c 'create database cyder_django' || [ \$RETRIES -eq 0 ]; do
    echo \"Waiting for postgres server, \$((RETRIES--)) remaining attempts...\"
    sleep 10
done
if [ \$RETRIES -eq 0 ]; then
    echo \"ERROR: Postgres server isn't responding after a minute! (or an other error occured)\"
    exit 1
fi
exit 0
"
docker-compose exec db bash -c "$CMD" &&
docker-compose up -d wsgi &&
docker-compose exec wsgi python manage.py migrate &&
docker-compose exec wsgi python manage.py collectstatic &&
echo "Creation of the django superuser (please answer):" &&
docker-compose exec wsgi python manage.py createsuperuser &&
docker-compose up -d http &&
DONE=1
if [ $DONE -eq 0 ]; then
    docker-compose stop
    echo "An error occured..."
    exit 1
fi
echo "Done!! All the containers are up and ready :)"
exit 0
