#!/bin/bash
# Djacket CLI script.

SCRIPTNAME="djacket.sh";
SCRIPTPATH=$(realpath $0);
SCRIPTDIR=$(dirname $SCRIPTPATH);

IN_RED="\033[0;31m";
IN_GRY="\033[0;44m";
IN_DEF="\033[0m";

# Generates a random string of desired length.
#   e.g.
#     random-string 16
function random-string {
    cat /dev/urandom | tr -dc 'a-zA-Z0-9!@#$%^&*()_+-=><?[]{}' | fold -w ${1:-32} | head -n 1
}

# Ask a yes/no question for confirmation.
function read_yes_no {
    printf "${IN_RED}[y|n] ${IN_DEF}";
    read yesno;
    while [[ "${yesno}" != "y" && "${yesno}" != "n" ]]
    do
        printf "${IN_RED}please answer [y|n] ${IN_DEF}";
        read yesno;
    done

    if [[ "${yesno}" == "n" ]]; then
        return 1;
    else
        return 0;
    fi
}

# Runs a regex check to see if the given port is valid.
function validate_port {
    if ! [[ ${port} =~ ^[1-9][0-9]{1,4}$ ]]; then
        echo ":$port is not a valid port.";
        echo "Example usage:";
        echo "  ./djacket.sh 8085"; echo;
        exit 1;
    fi
}

# Prints a message if Djacket is not installed.
function alert_if_not_installed {
    if ! is_installed; then
        echo;
        printf "${IN_GRY}.=----------------------------------------------=.\n";
        printf           "|                  Djacket CLI                   |\n";
        printf           ".=----------------------------------------------=.${IN_DEF}";
        echo;
        echo "  Apparently you haven't installed Djacket";
        echo "    or your environment variables are tampered.";
        echo "  Please run './djacket.sh' to get started.";
        echo;
        exit 1;
    fi
}

# Prints a list of commands with their description.
function script_help {
    printf "${IN_GRY}.=----------------------------------------------=.\n";
    printf           "|                  Djacket CLI                   |\n";
    printf           "|             Available Instructions             |\n";
    printf           ".=----------------------------------------------=.${IN_DEF}\n";
    echo;
    printf "${IN_RED}dev <port_number>${IN_DEF}\n";
    echo "  Starts development containers."; echo;
    printf "${IN_RED}prod${IN_DEF}\n";
    echo "  Starts production stack."; echo;
    printf "${IN_RED}stop${IN_DEF}\n";
    echo "  Stops production stack."; echo;
    printf "${IN_RED}logs${IN_DEF}\n";
    echo "  Tails production Docker containers logs."; echo;
    printf "${IN_RED}rm_dev${IN_DEF}\n";
    echo "  Removes development Docker containers."; echo;
    printf "${IN_RED}rm_dev_image${IN_DEF}\n";
    echo "  Removes development Docker image."; echo;
    printf "${IN_RED}rm_prod${IN_DEF}\n";
    echo "  Removes production Docker containers."; echo;
    printf "${IN_RED}rm_prod_image${IN_DEF}\n";
    echo "  Removes production Docker image."; echo;
    printf "${IN_RED}rm_frontend_builds${IN_DEF}\n";
    echo "  Removes all of frontend build files compiled by GulpJS."; echo;
    printf "${IN_RED}uninstall${IN_DEF}\n";
    echo "  Removes all the content and containers related to Djacket."; echo;
}

# Prompts user to input something with a message and an example
#   and puts the result in the given variable.
#
#     e.g.
#       prompt_user "log storage path" "(e.g. /path/to/smthing)" OUTPUT
function prompt_user {
    WHAT="$1";
    EXAMPLE="$2";
    OUTPUT_VAR="$3";
    ASKED_VAR="";
    while [ "$ASKED_VAR" == "" ]; do
        read -p "Enter $WHAT $EXAMPLE: " -e ASKED_VAR;
        if [[ "$ASKED_VAR" != "" ]]; then
            printf "${IN_RED}Do you confirm $ASKED_VAR for $WHAT? ${IN_DEF}";
            if ! read_yes_no; then
                ASKED_VAR="";
            fi
        fi
    done
    export "$OUTPUT_VAR"="$ASKED_VAR";
    echo;
}

# Returns state 0 if Djacket is installed else 1.
function is_installed {
    if [ -f "$SCRIPTDIR/.env" ]; then
        source "$SCRIPTDIR/.env";
        if [[ "$INSTALLED_IN" =~ ^[0-9]{10,11}$ ]]; then
            return 0;
        fi
    fi

    return 1;
}

# Initializes required environment variables.
function setup {
    if ! is_installed; then
        if [ -f "$SCRIPTDIR/.env" ]; then
            rm "$SCRIPTDIR/.env";
        fi
        touch "$SCRIPTDIR/.env";
        printf "${IN_GRY}.=----------------------------------------------=.\n";
        printf          "|                  Djacket CLI                   |\n";
        printf          "|   Welcome to the setup process for Djacket!    |\n";
        printf          "|      This won't take more than a minute.       |\n";
        printf          ".=----------------------------------------------=.${IN_DEF}\n";
        ask_for_envs;
        echo "INSTALLED_IN=$(date +%s)" >>  "$SCRIPTDIR/.env";
    fi
}

# Generates a random string and puts in environment variables
#   to be used in django settings.
function put_secret_key {
    echo "DSCT_KY='$(random-string 40)'" >> "$SCRIPTDIR/.env";
}

# Prompts user to enter required environment variables
#   for Djacket to start.
function ask_for_envs {
    echo;
    echo "  Asking for host details :->"; echo;
    ask_for_hostname;
    echo "Asking for app-required paths :->";
    echo "  If a path you entered didn't exist, It will be created."; echo;
    ask_for_paths;
    printf "Generating a secret for you... ";
    put_secret_key;
    printf "done \xE2\x9C\x94 \n";
    echo ">>> (We'are all set and ready to go.) <<<";
    echo;
}

# Asks user for host IP address and domain name.
function ask_for_hostname {
    prompt_user "your host IP address" "(e.g. 173.194.122.231)" DJHIPADDR;
    prompt_user "your host domain name" "(e.g. google.com)" DJHDOMNN;

    echo "DALWD_HSTS=['$DJHIPADDR','$DJHDOMNN']" >> "$SCRIPTDIR/.env";
}

# Asks user where to store database, repos, static and media files.
function ask_for_paths {
    prompt_user "database storage path" "/path/to/db" DJDBPATH;
    echo "DB_FOLDER=$DJDBPATH" >> "$SCRIPTDIR/.env";
    if [ -d "$DJDBPATH" ]; then
        mkdir -p "$DJDBPATH";
    fi

    prompt_user "git repositories storage path" "/path/to/deposit" DJDEPPATH;
    echo "DEPOSIT_FOLDER=$DJDEPPATH" >> "$SCRIPTDIR/.env";
    if [ -d "$DJDEPPATH" ]; then
        mkdir -p "$DJDEPPATH";
    fi

    prompt_user "collected static files path" "/path/to/static" DJSTTPATH;
    echo "STATIC_FOLDER=$DJSTTPATH" >> "$SCRIPTDIR/.env";
    if [ -d "$DJSTTPATH" ]; then
        mkdir -p "$DJSTTPATH";
    fi

    prompt_user "uploaded media files path" "/path/to/media" DJMEDPATH;
    echo "MEDIA_FOLDER=$DJMEDPATH" >> "$SCRIPTDIR/.env";
    if [ -d "$DJMEDPATH" ]; then
        mkdir -p "$DJMEDPATH";
    fi
}

# Stops the production Docker containers.
function stop {
    alert_if_not_installed;
    docker-compose -f docker-compose.prod.yml stop;
}

# Starts development Docker containers.
function dev {
    setup;
    export DJACKET_DEV_PORT=${port};
    docker-compose -f docker-compose.dev.yml build;
    docker-compose -f docker-compose.dev.yml up;
}

# Starts production stack.
function prod {
    setup;
    docker-compose -f docker-compose.prod.yml build;
    docker-compose -f docker-compose.prod.yml up -d;
}

# Tails production Docker containers logs.
function logs {
    alert_if_not_installed;
    docker-compose -f docker-compose.prod.yml logs -f;
}

# Removes development Docker containers.
function rm_dev {
    docker rm djacket_backend djacket_frontend djacket_dev_base;
}

# Removes development Docker image.
function rm_dev_image {
    docker rmi djacket_dev_image;
}

# Removes production Docker containers.
function rm_prod {
    docker rm djacket_web djacket_upstream djacket_prod_base;
}

# Removes production Docker image.
function rm_prod_image {
    docker rmi djacket_prod_image;
}

# Removes all of frontend build files compiled by GulpJS.
function rm_frontend_builds {
    sudo rm -rf "$SCRIPTDIR/core/frontend/public/build/";
    mkdir "$SCRIPTDIR/core/frontend/public/build/";
    touch "$SCRIPTDIR/core/frontend/public/build/.gitkeep";
}

# Removes environment variables, folders and Docker containers.
function uninstall {
    printf "${IN_GRY}This will remove all your files:\n";
    printf "  - Installed environment variables\n";
    printf "  - Entered folders for database, deposit, medias, etc\n";
    printf "  - Docker containers and images\n";
    printf "  - All your log and pid files${IN_DEF}\n";
    printf "${IN_RED}Do you confirm?";

    if read_yes_no; then
        source "$SCRIPTDIR/.env";
        sudo rm -rf "$DB_FOLDER" "$DEPOSIT_FOLDER" "$STATIC_FOLDER" "$MEDIA_FOLDER";
        rm_dev;
        rm_dev_image;
        rm_prod;
        rm_prod_image;
        rm_frontend_builds;
        sudo find "$SCRIPTDIR" -name "*.log" -delete;
        sudo find "$SCRIPTDIR" -name "*.pid" -delete;
        rm "$SCRIPTDIR/.env";
        printf "Uninstalled Djacket.\n";
    else
        printf "Uninstallation aborted.\n";
    fi
}

# Let's see what user wants.
if [[ "$1" == "dev" ]]; then
    port=${2};
    validate_port;
    dev;
elif [[ "$1" == "prod" ]]; then
    prod;
elif [[ "$1" == "stop" ]]; then
    stop;
elif [[ "$1" == "logs" ]]; then
    logs;
elif [[ "$1" == "rm_dev" ]]; then
    rm_dev;
elif [[ "$1" == "rm_dev_image" ]]; then
    rm_dev_image;
elif [[ "$1" == "rm_prod" ]]; then
    rm_prod;
elif [[ "$1" == "rm_prod_image" ]]; then
    rm_prod_image;
elif [[ "$1" == "rm_frontend_builds" ]]; then
    rm_frontend_builds;
elif [[ "$1" == "uninstall" ]]; then
    uninstall;
else
    script_help;
fi
