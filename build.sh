#! /usr/bin/env bash

. ./common.sh &&
docker build --build-arg USER_ID=${USER_ID} --build-arg GROUP_ID=${GROUP_ID} -t ${NAME}:${VERSION} . &&
docker tag ${NAME}:${VERSION} ${NAME}:latest &&
docker system prune -f
