DJANGO_WSGI_MODULE=docker_django.config.wsgi            # WSGI module name

# Start your Django Unicorn
exec /usr/local/bin/gunicorn ${DJANGO_WSGI_MODULE}:application -w 2 -b :8000
