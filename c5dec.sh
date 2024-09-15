#!/bin/bash
echo Starting C5-DEC CAD...

# Define variables
USER=root
CONTAINER_NAME=c5dec-container
IMAGE_NAME=c5dec:v0.2.0

# Define volume mounts
C5_VOLUME=$(pwd)/c5dec:/home/$USER/c5dec/c5dec
DOCS_VOLUME=$(pwd)/docs:/home/$USER/c5dec/docs

if [ "$#" -lt 1 ]
then
    # Run the Docker container with no argument: pass the -h argument to c5dec
    docker run -it --rm --name $CONTAINER_NAME \
        -v $C5_VOLUME \
        -v $DOCS_VOLUME \
        --network host \
        $IMAGE_NAME -h 
else
    # Run the Docker container with the user-specified arguments
    docker run -it --rm --name $CONTAINER_NAME \
        -v $C5_VOLUME \
        -v $DOCS_VOLUME \
        -p 5432:5432 \
        $IMAGE_NAME "$@"
fi