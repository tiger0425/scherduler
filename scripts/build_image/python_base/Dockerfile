FROM ubuntu:14.04

RUN  rm /etc/apt/sources.list
# use the tshua source
COPY sources.list /etc/apt/sources.list

RUN  apt-get update -y \
    && apt-get install -y wget \
    && wget https://bootstrap.pypa.io/get-pip.py \
    && apt-get install -y python \
    && python get-pip.py \
    && apt-get install -y --no-install-recommends\
               python-dev \
               libkrb5-dev \
               libsasl2-dev \
               libssl-dev \
               libffi-dev \
               build-essential \
               libblas-dev \
               liblapack-dev \


