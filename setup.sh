#!/bin/bash

set -e 

if [ $(id -u) -ne "0" ]
then
	echo "Please run as root"
	exit
fi

CONTAINER_NAME="STM_CONT"
IMAGE_NAME="STM_IMG"

if [ $# -ge 1 ]; then
	IMAGE_NAME="${1}_IMG"
	CONTAINER_NAME="${1}_CONT"
fi

#containers/image in lowercase
CONTAINER_NAME=$(echo $CONTAINER_NAME | tr '[:upper:]' '[:lower:]')
IMAGE_NAME=$(echo $IMAGE_NAME | tr '[:upper:]' '[:lower:]')


echo "image will be named : $IMAGE_NAME"
echo "container will be named : $CONTAINER_NAME"

# stop and remove an homonyme container 
HOMONYME=$(sudo docker ps -a | grep $CONTAINER_NAME | cut -d' ' -f1)

if [ ! -z $HOMONYME ]; then
	echo "removing : $HOMONYME"
	sudo docker stop $HOMONYME
	sudo docker rm $HOMONYME
fi

# create the image
echo "--- building the image ---"
sudo docker build -t $IMAGE_NAME .
echo "launching the container in interractive mode"
sudo docker run -it --name $CONTAINER_NAME $IMAGE_NAME /bin/bash