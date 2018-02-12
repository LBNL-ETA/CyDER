FROM python

WORKDIR /usr/src/app
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD ./ /usr/src/app

CMD ["celery", "-A", "sim_worker", "worker", "-l", "info", "-c", "1", "-Q", "sim_worker"]
