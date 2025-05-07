#!/bin/bash
PROJECT_NAME=c5dec

echo Building $PROJECT_NAME images...
docker build -t $PROJECT_NAME:v1.0 .
docker build -f dev.Dockerfile -t $PROJECT_NAME-dev:v1.0 .