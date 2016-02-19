#!/bin/bash

CURRENTDIR=$(readlink -f "$0")
DJACKETPATH=$(dirname "${CURRENTDIR}")
SEK=`python3 -c 'import random; import string; print ("".join([random.SystemRandom().choice(string.digits + string.ascii_letters + "!@#$%^&*()_+-=><?[]{}") for i in range(64)]))'`


function prepare_environment () {
    export PYTHONPATH=$PYTHONPATH:${DJACKETPATH}/libs;
}


function issue_error () {
    printf "\n\033[31m----------------------------------------------------------------\033[m\n";
    printf "\n\033[31mBad Luck! \nPlease fix happened issues and run the script again.\033[m\n";
    exit 1;
}


function read_yes_no () {
    printf "[yes|no] "
    read yesno;
    while [[ "${yesno}" != "yes" && "${yesno}" != "no" ]]
    do
        printf "please answer [yes|no] "
        read yesno;
    done

    if [[ "${yesno}" == "no" ]]; then
        return 1;
    else
        return 0;
    fi
}


function print_djacket () {
    cat ${DJACKETPATH}/SIGN;
}


function welcome () {
    clear;
    print_djacket;
    echo;
    echo;
    echo '             Welcome to Djacket v0.1.0 installation script';
    echo '.----------------------------------------------------------------------.';
    echo '| In order to have a successful installation you need to have:         |';
    echo '|                                                                      |';
    echo '|  - Git >= v1.8 (http://git-scm.com)                                  |';
    echo '|  - Python >= 3.x (http://python.org)                                 |';
    echo '|  - Pillow imaging library (https://pypi.python.org/pypi/Pillow)      |';
    echo '|                                                                      |';
    echo '| installed and configured properly.                                   |';
    echo '|                                                                      |';
    echo '| If these requirements are not met, Please install them first,        |';
    echo '|    then run this script again.                                       |';
    echo '.----------------------------------------------------------------------.';
    printf '                All set? Should we continue?  ';
    if ! read_yes_no; then
        exit 0;
    fi
}


function chk_reqs () {
    echo;
    if ! which git 2>/dev/null 1>&2; then
        echo 'Git not found.';
        issue_error;
    fi
    if ! which python3 2>/dev/null 1>&2; then
        echo 'Python 3.x not found.';
        issue_error;
    fi
    if ! which pip3 2>/dev/null 1>&2; then
        echo 'pip3 package manager (part of Python 3.x) not found.';
        issue_error;
    fi
    if ! python -c "from PIL import Image"; then
        echo 'Pillow is not installed.';
        issue_error;
    fi
    if ! which gunicorn 2>/dev/null 1>&2; then
        echo 'Installing Gunicorn ----------------------------------------- [ STARTED ]';
        sudo pip3 install gunicorn
        echo 'Installing Gunicorn ----------------------------------------- [ DONE ]';
    fi
    printf "\nRequirements all met ---------------------------------------- [ OK ]\n";
}


function setup_deposit () {
    echo;
    echo 'Creating deposit folder --------------------------------------- [ STARTED ]';
    echo;
    echo 'This folder is where your repositories will be kept';
    echo "It's highly recommended for this folder to be outside of installation folder ";
    echo "  where you have read/write access privileges.";
    echo;
    printf "Deposit folder path: ";
    read deposit_path;
    mkdir "${deposit_path}";
    echo 'Deposit folder created ---------------------------------------- [ DONE ]';
}


function setup_django () {
    echo;
    echo 'Installing Djacket -------------------------------------------- [ STARTED ]';
    prepare_environment;
    echo "GIT_DEPOSIT_ROOT = '${deposit_path}'" >> ${DJACKETPATH}/core/backend/djacket/settings.py;
    cd ${DJACKETPATH}/core/backend;
    ./manage.py makemigrations;
    ./manage.py migrate;
    ./manage.py collectstatic --noinput;
    echo;
    echo;
    echo 'Creating super user -------------------------------------------- [ STARTED ]';
    echo;
    echo 'A super user should be created for management and administration';
    echo '  Please provide requested information to create one.';
    ./manage.py createsuperuser;
    cd ../..;
    chmod +x djacket.sh;
    echo;
    echo 'Installing Djacket -------------------------------------------- [ DONE ]';
}


function setup_security () {
    echo;
    echo 'Setting up security -------------------------------------------- [ STARTED ]';
    echo;
    echo 'These settings here will affect your Djacket server security so Please follow the instructions exactly.';
    echo "Enter your server IP address or domain name or both in one of these formats";
    echo "  e.g.";
    echo "      123.123.123.123";
    echo "      www.example.com";
    echo "      .example.com";
    echo;
    printf  "IP address/domain name: ";
    read thishost;
    echo;
    printf "You entered '${thishost}' as your host. Do you confirm?  ";
    if ! read_yes_no; then
        echo "Please enter your server IP address or domain name in correct format.";
        printf  "IP address/domain name: ";
        read thishost;
    fi
    echo;
    echo "ALLOWED_HOSTS = ['${thishost}']" >> ${DJACKETPATH}/core/backend/djacket/settings.py;
    echo 'Added your host/domain name to settings.py --------------------- [ DONE ]';
    echo;
    echo 'Installing secret key ------------------------------------------ [ STARTED ]';
    echo;
    echo "SECRET_KEY = '$SEK'" >> ${DJACKETPATH}/core/backend/djacket/settings.py;
    echo 'Installing secret key ------------------------------------------ [ DONE ]';
    echo;
    echo 'Setting up security -------------------------------------------- [ DONE ]';
    echo;

}


function djacket_ready () {
    printf "\n\n\n";
    echo "$(date)" > ${DJACKETPATH}/run/INSTALLATION;
    echo '                      v0.1.0 successfully installed';
    echo '.--------------------------------------------------------------------------.';
    echo '|                                                                          |';
    echo '| You can now start Djacket by executing "./djacket.sh start port_number"  |';
    echo '|     e.g.                                                                 |';
    echo '|         ./djacket.sh start 8080                                          |';
    echo '|                                                                          |';
    echo '.--------------------------------------------------------------------------.';
    echo;
    printf "\n\033[33mYour web server should point to these locations after installation:\033[m\n";
    echo '------------------------------------------------------------------------';
    printf "\033[33m    /static location should be set to: ${DJACKETPATH}/core/static/ \033[m\n";
    printf "\033[33m    /media location should be set to: ${DJACKETPATH}/core/media/ \033[m\n";
    echo '------------------------------------------------------------------------';
    printf "\033[33mRead more about configurations on http://github.com/Djacket/djacket \033[m\n";
    echo;
}


print_djacket;
welcome;
chk_reqs;
setup_deposit;
setup_security;
setup_django;
djacket_ready;
