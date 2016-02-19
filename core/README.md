# Djacket /core

This folder contains core application.

## /backend
Django project is inside this folder with all the applications.
Apps inside are:

- djacket: main Django project folder.
- filter: creates custom Djacket template filters.
- git: Djacket's Git library for interactions
    with repositories.
- repository: creates/modifies repositories.
- user: creates/modifies users and their profiles.
- utils: has extra tools useful across the whole project.

If using default settings from installation script [SQLite](https://www.sqlite.org/) database file will be kept here. PostgreSQL database settings are available in settings.py for a more advanced database approach.

## /frontend
Contains view and static files for development and production. All styles, scripts and views templates are developed under /public/dev folder then using ["gulp"](http://gulpjs.com/) tasks they are compiled and pushed to /public/build path for production.
For any customization, first make sure you have
[nodejs](https://nodejs.org/en/) and gulp installed globally then  inside /frontend folder, run

```
    npm install
```

Now you can make changes to gulpfile and commit them.
[Bower](http://bower.io/) configurations are available as well in ".bowerrc" file.
For any customization, inside /frontend folder first run

```
    bower install
```

then you can make changes to frontend libraries such as [jQuery](https://jquery.com/), [Chart.js](www.chartjs.org/), [Font-Awesome](https://fortawesome.github.io/Font-Awesome/), etc.

## /media
As of right now only user avatar images are kept are.

## /static
Contains static files. All static files will be piled up in here after installation script executes 'collectstatic'.
Webserver's (Apache, Nginx, etc) "/static" location should be pointed to this folder.
If there's a need for changing static folder, you can change variable 'STATIC_ROOT' in backend/djacket/settings.py and run

```
    ./manage.py collectstatic
```

Note that your Webserver's settings should be changed then too.
