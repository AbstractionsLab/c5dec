#!/bin/bash
echo C5-DEC CAD cleaning up...
docker stop c5dec-container || true && docker rm c5dec-container
docker rmi c5dec:v1.0
docker stop c5dec-dev-container || true && docker rm c5dec-dev-container
docker rmi c5dec-dev:v1.0
echo Done.