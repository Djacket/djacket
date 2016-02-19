# Installation / Troubleshooting

Here the whole process of Djacket installation is explained so in case you feel to do a manual
    installation or want to solve problems occurred along the way, the path would be clear.
Process is as explained below in following sub-sections.


## Requirements
Djacket requires
```
- Git (version 1.8 or above)
- Python3 and pip3 (any version of Python version 3.x)
- Pillow imaging library (https://pypi.python.org/pypi/Pillow)
```
to be installed and working.

Other libraries will be exported during installation and start.
These requirements will be checked at the beginning of installation.


## Deposit
There should be an absolute path for a folder to keep Git repositories on server. Path for this folder
    is set to variable GIT_DEPOSIT_ROOT in 'core/backend/djacket/settings.py' for Django runtime like this:

```
    GIT_DEPOSIT_ROOT = '/path/to/your/deposit/folder'
```

This path will be set during running of installation script.

Each user will have a folder inside GIT_DEPOSIT_ROOT with his/her username
    as the folder name and inside this folder is owner's repositories.

So for example if user's username is "thomas", his repositories will be kept under
```
    GIT_DEPOSIT_ROOT/thomas/
```

If you decided to change path of this folder make sure to move all users repositories.


## Django Server Application
Next, python environment variable PYTHONPATH will be set to "/libs" folder so Djacket can
    run successfully with it's runtime libraries paths provided.
After that Django "manage.py" actions should run. These actions are committed using these commands:
```
./manage.py makemigrations
./manage.py migrate
./manage.py collectstatic
./manage.py createsuperuser
```
During these, database migrations, collection of static files and creation of super user are done.


## Security
There are some security considerations that should be done.
First user should enter their server IP address or domain name in one of formats accepted by Django framework
to be provided in ALLOWED_HOSTS variable in "core/backend/djacket/settings.py" like this:
```
ALLOWED_HOSTS = ['.example.com']
or
ALLOWED_HOSTS = ['www.example.com']
or
ALLOWED_HOSTS = ['123.123.123.123']
```
Then Django secret key is generated and put to "core/backend/djacket/settings.py":
```
    SECRET_KEY = 'some random generated string'
```
During installation a random secret key will be generated automatically and installed.


## Ready
Now your Djacket application is completely setup.
The only thing here is configuring the web server to host application, static and media files.
Nginx is the recommended web server. If you already have Apache installed on your server there's no problem for these two to work along since your Nginx configuration will not conflict with Apache if you do it right.

An example of Nginx configuration is shown below. Assuming that you started Djacket on port 8080 with command:

```
./djacket.sh start 8080
```
then you can configure Nginx to have a server as:

```
server {
	listen 8585;
	server_name example.com;
	client_max_body_size 32M;  # Maximum acceptable payload for an upload. If more than 32MB is needed, change it to higher values.

	location / {
        proxy_set_header Host $http_host;
		proxy_pass http://0.0.0.0:8080;  # Port number Djacket is started on.
	}

    location /media {
        alias /path/to/djacket-v0.1.0/core/media/;
    }

    location /static {
        alias /path/to/djacket-v0.1.0/core/static/;
    }
}
```

Now if you visit http://example.com:8585, you have a fully functioning Djacket.

# Other configurations
You can also deploy Djacket using other technologies such as Apache/mod_wsgi or Nginx/uwsgi, although installation script
    prefers Nginx/gunicorn.

Nevertheless if you prefer other stacks, everything is the same up until "Ready" section.
When you reach "Ready" section your Djacket Django application is fully functional and is kept under "core" folder.
Now you can deploy it as a Django application using Apache/mod_wsgi or Nginx/uswgi, etc.
