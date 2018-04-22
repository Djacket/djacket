FROM python:3.6

LABEL maintainer="Moeen Zamani <moeen.zamani@gmail.com>"

RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get install -y \
        nodejs \
        git \
        build-essential

RUN npm install -g gulp

WORKDIR /srv

ADD requirements.txt /srv/requirements.txt
RUN pip install -r requirements.txt

COPY package.json /srv/package.json
COPY package-lock.json /srv/package-lock.json
RUN npm install

COPY ./core/backend/ /srv/core/backend/
COPY ./core/frontend/ /srv/core/frontend/

COPY ./SIGN /srv/SIGN
COPY ./docker-entrypoint-build.sh /srv/docker-entrypoint-build.sh

WORKDIR /srv/core
