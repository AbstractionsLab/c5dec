#!/bin/bash
echo Starting C5-DEC CAD...
echo For usage instructions, run: ./c5dec.sh help

# Define variables
USER=alab
CONTAINER_NAME=c5dec-container
IMAGE_NAME=c5dec:v1.0

DEV_CONTAINER_NAME=c5dec-dev-container
DEV_IMAGE_NAME=c5dec-dev:v1.0

PQC_CONTAINER_NAME=c5dec-pqc-container
PQC_IMAGE_NAME=openquantumsafe/oqs-ossl3:latest

# Define volume mounts
C5_VOLUME=$(pwd):/home/$USER/c5dec

if [ "$#" -lt 1 ]
then
    # Run the Docker container with no argument: pass the -h argument to c5dec
    echo Opening C5-DEC CLI help...
    docker run -it --rm --name $CONTAINER_NAME \
        -v $C5_VOLUME \
        --network host \
        $IMAGE_NAME -h 
elif [ "$1" == "session" ]
then
    # Create the Docker container and open a session for interactive use
    echo Launching an interactive C5-DEC CAD session...
    # if the user volume is not specified, use the default
    # Check if the user volume is specified
    if [ -z "$2" ]
    then
        echo "No user directory specified. Using default: /home/$USER/c5dec/workspace"
        echo "Host directory $(pwd)/workspace mapped to container directory /home/$USER/c5dec/workspace"
        USER_VOLUME=$(pwd)/workspace:/home/$USER/workspace
    else
        echo "User directory specified: $2"
        echo "Host directory $2 mapped to container directory /home/$USER/workspace"
        USER_VOLUME=$2:/home/$USER/workspace
    fi
    # Check if the user volume is mounted
    docker run -it --rm --name $DEV_CONTAINER_NAME \
        -v $C5_VOLUME \
        -v $USER_VOLUME \
        -p 5432:5432 \
        $DEV_IMAGE_NAME /bin/bash
elif [ "$1" == "pqc" ]
then
    # Run the OQS-OpenSSL provider Docker container
    echo Launching C5-DEC PQC container: OQS-OpenSSL provider...
    docker run -it --rm --name $PQC_CONTAINER_NAME \
        -v $C5_VOLUME \
        --network host \
        $PQC_IMAGE_NAME /bin/ash
elif [ "$1" == "help" ]
then
    echo ---
    echo ./c5dec.sh
    echo ... to open the C5-DEC CLI help menu
    echo ./c5dec.sh session \<user_directory\>
    echo ... to start an interactive C5-DEC session
    echo ./c5dec.sh pqc
    echo ... to use the OQS-OpenSSL provider
    echo ./c5dec.sh \<command\>
    echo ... to run a C5-DEC CLI command
    echo ./c5dec.sh \<command\> -h
    echo ... to get help for a C5-DEC CLI command
    echo ---
else
    # Run the Docker container with the user-specified arguments
    echo Executing C5-DEC CAD CLI command $1...
    docker run -it --rm --name $CONTAINER_NAME \
        -v $C5_VOLUME \
        -p 5432:5432 \
        $IMAGE_NAME "$@"
fi