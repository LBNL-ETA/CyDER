FROM python:3.4.3

WORKDIR /usr/src/at-build
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /usr/src/app
CMD ["celery", "-A", "celery_test", "worker", "-l", "info"]
