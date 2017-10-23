FROM python

WORKDIR /usr/src/at-build

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN apt-get update
RUN apt-get install -y supervisor
RUN systemctl enable supervisor.service

COPY ./celery_beat.conf /etc/supervisor/conf.d/celery_beat.conf
COPY ./celery_worker.conf /etc/supervisor/conf.d/celery_worker.conf

WORKDIR /usr/src/init/
COPY ./init.sh init.sh
CMD ["./init.sh"]
