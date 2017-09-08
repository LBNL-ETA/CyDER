docker-compose up -d db &&
docker-compose exec db psql -h 127.0.0.1 -U postgres -w -c 'create database cyder_django' &&
docker-compose up -d wsgi &&
docker-compose exec wsgi python manage.py collectstatic &&
docker-compose exec wsgi python manage.py migrate &&
docker-compose stop
