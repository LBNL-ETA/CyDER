FROM python

WORKDIR /usr/src/at-build

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN apt-get update
RUN apt-get install -y supervisor
RUN systemctl enable supervisor.service

COPY ./celery_beat.conf /etc/supervisor/conf.d/celery_beat.conf
COPY ./celery_worker.conf /etc/supervisor/conf.d/celery_worker.conf

COPY ./init.sh init.sh

WORKDIR /usr/src/app/
CMD ["/usr/src/at-build/init.sh"]
