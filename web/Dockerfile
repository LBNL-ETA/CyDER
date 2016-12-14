FROM python:2.7-onbuild

# Installing Vim to open files
RUN apt-get update
RUN echo "y" | apt-get install vim

# Installing sudo
RUN echo "y" | apt-get install sudo

# Install supervisor to manage all the processes
RUN echo "y" | apt-get install supervisor

# Copy the settings files for the server and celery beat processes
COPY web_framework.conf /etc/supervisor/conf.d/
COPY celery_beat.conf /etc/supervisor/conf.d/
COPY celery_worker.conf /etc/supervisor/conf.d/
