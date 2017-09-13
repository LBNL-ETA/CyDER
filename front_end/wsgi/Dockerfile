FROM python

WORKDIR /usr/src/at-build

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /usr/src/app/
CMD ["gunicorn", "--reload", "config.wsgi", "-b", "0.0.0.0:8000"]
