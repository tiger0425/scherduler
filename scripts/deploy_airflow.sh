#!/usr/bin/env bash

# delete the old the one
rm -rf ./deploy_image/airflow/dags
cp -r ../dags  ./deploy_image/airflow/dags
cd ./deploy_image/airflow/


sudo docker-compose down
sudo docker-compose up -d