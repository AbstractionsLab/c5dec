#!/bin/bash
echo C5-DEC CAD cleaning up...
docker stop c5dec-container || true && docker rm c5dec-container
docker rmi c5dec:v0.2.0
echo Done.