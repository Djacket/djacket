#!/bin/bash

CURRENTDIR=$(readlink -f "$0")
DJACKETPATH=$(dirname "${CURRENTDIR}")

gunicorn_conf=${DJACKETPATH}/run/djacket.gunicorn.conf
pidfile=${DJACKETPATH}/run/djacket.pid


function chk_reqs () {
    echo;
    if ! which git 2>/dev/null 1>&2; then
        echo 'Git not found. Please install Git, then run the script again.';
        issue_error;
    fi
    if ! which python3 2>/dev/null 1>&2; then
        echo 'Python 3.x not found. Please install Python 3.x, then run the script again';
        issue_error;
    fi
    if ! which pip3 2>/dev/null 1>&2; then
        echo 'pip3 package manager (part of Python 3.x) not found. Please install pip3, then run the script again';
        issue_error;
    fi
    if ! which gunicorn 2>/dev/null 1>&2; then
        echo 'Installing Gunicorn ------------------------------------------------ [ STARTED ]';
        sudo pip3 install gunicorn
        echo 'Installing Gunicorn ------------------------------------------------ [ DONE ]';
    fi
    printf "\nRequirements all met ------------------------------------------- [ OK ]\n";
}


function chk_installation () {
    printf "Installation date: ";
    if ! cat $DJACKETPATH/run/INSTALLATION; then
        echo "Seems like you haven't run 'setup-djacket.sh' file for installation";
        echo "Please do it by executing 'bash setup-djacket.sh', then run the script again";
        echo;
        exit 1;
    else
        echo;
    fi
}


function prepare_environment () {
    export PYTHONPATH=$PYTHONPATH:${DJACKETPATH}/libs;
}


function validate_port () {
    if ! [[ ${port} =~ ^[1-9][0-9]{1,4}$ ]] ; then
        printf "\033[033m${port}\033[m is not a valid port number\n\n";
        exit 1
    fi
}


function is_djacket_running () {
    if pgrep -f "${gunicorn_conf}" 2>/dev/null 1>&2; then
        echo "Djacket is already running."
        exit 1;
    fi
}


function start_djacket () {
    chk_installation;
    echo "Starting Djacket v0.1.0 on port '${port}' ...";
    prepare_environment;
    cd core/backend;
    gunicorn djacket.wsgi:application -c "${gunicorn_conf}" -b 0.0.0.0:"${port}";
    cd ../..;
    sleep 3
    if ! pgrep -f "${gunicorn_conf}" 2>/dev/null 1>&2; then
        printf "\033[33mError:Djacket failed to start.\033[m\n"
        echo "Please try to run \"./djacket.sh start\" again"
        exit 1;
    fi
    echo;
    echo "Djacket started successfully.";
    echo;
}


function stop_djacket () {
    echo;
    if [[ -f ${pidfile} ]]; then
        pid=$(cat "${pidfile}")
        echo "Stopping Djacket ...";
        echo;
        kill ${pid}
        rm -f ${pidfile}
        echo "Djacket stopped successfully.";
        return 0
    else
        echo "Djacket is stopped."
    fi
    echo;
}


if [[ $1 != "start" && $1 != "stop" && $1 != "restart" ]]; then
    echo;
    echo 'You can start/stop/restart Djacket by running one of these commands';
    echo './djacket.sh start port_number';
    echo './djacket.sh stop';
    echo './djacket.sh restart';
    echo '    e.g.';
    echo '        ./djacket start 8080';
    echo '        ./djacket stop';
    echo '        ./djacket restart 8585';
    echo;
else
    if [[ $1 == "start" ]]; then
	port=${2}
	validate_port;
        is_djacket_running;
        start_djacket;
    elif [[ $1 == "stop" ]]; then
        stop_djacket;
    elif [[ $1 == "restart" ]]; then
        if [[ $2 == "" ]]; then
            echo "Port for restarting server is not specified";
        else
            port=${2};
            validate_port;
            stop_djacket;
            sleep 3;
            is_djacket_running;
            start_djacket;
        fi
    else
        echo;
    fi
fi
