#!/bin/bash
echo Starting C5-DEC CAD...

if [ "$#" -lt 1 ]
then
    docker run --rm -it -v ./c5dec:/home/root/c5dec/c5dec c5dec -h
else
    docker run --rm -it -v ./c5dec:/home/root/c5dec/c5dec -p 5432:5432 c5dec "$@"
fi