#!/usr/bin/env bash

VERSION=0.0.1

cd ./build_image/airflow/

sudo docker build -t registry.cn-hangzhou.aliyuncs.com/brucedone/airflow:v$VERSION .
sudo docker push registry.cn-hangzhou.aliyuncs.com/brucedone/airflow:v$VERSION