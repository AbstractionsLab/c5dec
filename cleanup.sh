#!/bin/bash
echo C5-DEC CAD cleaning up...
docker stop 5dec || true && docker rm c5dec
docker rmi c5dec
echo Done.