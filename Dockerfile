FROM python:3.6

LABEL maintainer="Moeen Zamani <moeenzdev@gmail.com>"

RUN apt-get update && apt-get install -y \
        git \
        nodejs-legacy \
        npm

RUN npm install -g gulp

WORKDIR /srv

ADD requirements.txt /srv/requirements.txt
RUN pip install -r requirements.txt

COPY package.json /srv/package.json
RUN npm install

COPY ./core/backend/ /srv/core/backend/
COPY ./core/frontend/ /srv/core/frontend/

COPY ./SIGN /srv/SIGN
COPY ./docker-entrypoint-build.sh /srv/docker-entrypoint-build.sh

WORKDIR /srv/core
