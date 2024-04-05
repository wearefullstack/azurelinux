#!/bin/bash

# output = tensorboard-$TB_VERSION-cache.tar.gz
# Tensorboard version to use
TB_VERSION="2.16.2"

docker build --build-arg TB_VERSION=$TB_VERSION -t tensorboard_image .

CONTAINER_ID=$(docker run -d tensorboard_image)

docker cp $CONTAINER_ID:/root/tensorboard-$TB_VERSION-cache.tar.gz $PWD

docker stop $CONTAINER_ID
docker rm $CONTAINER_ID
