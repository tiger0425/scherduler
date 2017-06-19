FROM registry.cn-hangzhou.aliyuncs.com/brucedone/python:base

ARG AIRFLOW_HOME=/workspace/airflow

RUN  rm /etc/apt/sources.list
COPY ./config/sources.list /etc/apt/sources.list

#prepare env
RUN  apt-get update -yqq \
    && apt-get install -yqq --no-install-recommends\
               python-dev \
               libkrb5-dev \
               libsasl2-dev \
               libssl-dev \
               libffi-dev \
               build-essential \
               libblas-dev \
               liblapack-dev \
               libpq-dev  \
    && mkdir -p /scheduler/log \
    && mkdir -p ${AIRFLOW_HOME}

COPY ./requirements.txt .
COPY script/entrypoint.sh /entrypoint.sh

RUN pip install -i 'http://mirrors.aliyun.com/pypi/simple/' -r ./requirements.txt --trusted-host mirrors.aliyun.com
WORKDIR ${AIRFLOW_HOME}


COPY config/airflow.cfg ${AIRFLOW_HOME}/airflow.cfg
ENV AIRFLOW_HOME /workspace/airflow
EXPOSE 8080 5555 8793
ENTRYPOINT ["/entrypoint.sh"]