# Dockerfile
FROM python:3.10-slim-buster

# Copy app files
RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/senseimenu
COPY . /opt/app/senseimenu/

WORKDIR /opt/app/senseimenu

# install python dependencies
RUN apt update
RUN apt-get -y update \
    && apt-get install -y \
        fonts-font-awesome \
        libffi-dev \
        libgdk-pixbuf2.0-0 \
        libpango1.0-0 \
        python-dev \
        python-lxml \
        shared-mime-info \
        libcairo2 \
    && apt-get -y clean
RUN pip install -r requirements.txt

# run gunicorn
CMD gunicorn senseimenu.wsgi:application --bind 0.0.0.0:$PORT
