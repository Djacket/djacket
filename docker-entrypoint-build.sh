#!/bin/bash
# Djacket build docker entrypoint shell script.

npm link gulp;

# GulpJS does the compiling of static files.
gulp --gulpfile ./frontend/gulpfile.js compile;

# If we are in development mode then we need to run 'makemigrations'
#   otherwise 'migrate' would suffice.
if [[ "$DJKR_MODE" == "dev" ]]; then
    python ./backend/manage.py makemigrations;
fi

# Keeping the database updated.
python ./backend/manage.py migrate;

# This will create an admin user if there is not any.
python ./backend/manage.py create_admin;    

# If we are in production we have to collect all the required static files.
if [[ "$DJKR_MODE" == "prod" ]]; then
    python ./backend/manage.py collectstatic --noinput;
fi

# We need to create some stock avatars first.
if [ ! -d "/srv/media/avatars" ]; then
    mkdir -p "/srv/media/avatars";
fi

# Here we download some stock avatars.
stock_avatars=3
if [ ! -d "/srv/media/stock" ]; then
    mkdir -p "/srv/media/stock";
    for i in $(seq $stock_avatars $END); do
        curl -m 5 "https://api.adorable.io/avatars/200/$i.png" > "/srv/media/stock/$i.png";
    done
else
    if [[ "$(ls /srv/media/stock | wc -l)" != "$stock_avatars" ]]; then
        for i in $(seq $stock_avatars $END); do
            curl -m 5 "https://api.adorable.io/avatars/200/$i.png" > "/srv/media/stock/$i.png";
        done
    fi
fi

cat /srv/SIGN;
