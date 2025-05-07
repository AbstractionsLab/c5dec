#!/bin/bash
echo Building c5dec images...
docker build -t c5dec:v1.0 .
docker build -t c5dec-dev:v1.0 -f dev.Dockerfile .