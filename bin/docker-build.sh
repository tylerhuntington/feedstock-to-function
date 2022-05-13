#!/bin/bash -xe

export DOCKER_BUILDKIT=1

sudo -E docker build \
    --pull \
    -f 'Dockerfile' \
    -t 'cr.ese.lbl.gov/ese/ftf-app' \
    .
