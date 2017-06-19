#!/usr/bin/env bash

VERSION=0.0.2

cd ./build_image/scheduler/

sudo docker build -t registry.cn-hangzhou.aliyuncs.com/brucedone/airflow:v$VERSION .
sudo docker push registry.cn-hangzhou.aliyuncs.com/brucedone/airflow:v$VERSION