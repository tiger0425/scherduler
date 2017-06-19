#!/usr/bin/env bash

# delete the old the one
rm -rf ./deploy_image/scheduler/dags
cp -r ../dags  ./deploy_image/scheduler/dags
cd ./deploy_image/scheduler/


sudo docker-compose down
sudo docker-compose up -d