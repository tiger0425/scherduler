#!/usr/bin/env bash

cd ./build_image/airflow/

sudo docker build -t airflow_bruce .
sudo docker pull