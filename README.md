# Djacket
A Git server written in [Python/Django](https://www.djangoproject.com/). It's meant to be for personal
or small business usages. Installation is available and tested for Linux servers.

<p align="center">
	<img src="index.png" alt="Index"/>
</p>


# Requirements
Djacket requires these packages:
```
- Git (version 1.8 or above)
- Python3 and pip3 (any version of Python version 3.x)
- Pillow imaging library (https://pypi.python.org/pypi/Pillow)
```
to be installed and working.


# Installation
Download latest release from https://github.com/Djacket/djacket/releases/latest, then extract and install:
```
tar xzvf djacket-v0.1.0.tar.gz
cd djacket-v0.1.0
sudo bash setup-djacket.sh
```
after installation you can start Djacket by running
```
./djacket.sh start 8080
```
Your web server should be configured to serve Djacket and it's static and media files. After installation, folder path for
static and media files is printed out for server settings. [Nginx](http://nginx.org/en/) is the recommended web server (and it can work along with your existing installation of Apache too).
In your Nginx configuration put (assuming your domain is example.com):
```
server {
	listen 8585;
	server_name example.com;
	client_max_body_size 32M;

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


For more details, troubleshooting or manual installation see [INSTALL](./INSTALL.md) file.


# Contribution
Djacket's backend technology is [Python/Django](https://www.djangoproject.com/) v1.8. aside from this, libraries:
```
python-dateutil
django-easy-pjax
```
are used, so if you want to make changes to backend you need these installed. These libraries will be provided inside libs
folder for each release.

Frontend is maintained using [gulpjs](http://gulpjs.com/) and [bower](http://bower.io/), so first make sure you have
[nodejs](https://nodejs.org/en/) and gulp installed globally then inside core/frontend, run
```
npm install
```
Now you can make changes to frontend views, styles and scripts by modifying files in core/frontend/public/dev.
Any changes you make will be compiled by gulp and pushed to build folder. So if you made any changes make sure to do
```
gulp compile
```
which runs the compilation task or if you are on constant development run
```
gulp
```
so default task will run (which is watching for file changes and pushing them to build folder)


# Issues
If you encountered any bugs or issues, Please report it either in Github issues section or send it as
an email to [projectdjacket@gmail.com](mailto:projectdjacket@gmail.com)


# Documentation
Project is fully documented and it can be reached by going to:
```
/admin/doc/
```
"docutils" package is required for browsing through.


# License

The MIT License (MIT)

Copyright (c) 2016 Djacket Project.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
