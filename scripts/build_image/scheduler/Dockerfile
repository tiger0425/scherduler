FROM registry.cn-hangzhou.aliyuncs.com/brucedone/python:stable

ENV AIRFLOW_HOME /workspace/airflow

COPY config/airflow.cfg ${AIRFLOW_HOME}/airflow.cfg
COPY ./config/sources.list /etc/apt/sources.list
COPY ./requirements.txt .
COPY script/entrypoint.sh /entrypoint.sh


#prepare env
RUN    mkdir -p /scheduler/log \
    && mkdir -p ${AIRFLOW_HOME}

RUN pip install -i 'http://mirrors.aliyun.com/pypi/simple/' -r ./requirements.txt --trusted-host mirrors.aliyun.com

WORKDIR ${AIRFLOW_HOME}
EXPOSE 8080 5555 8793
ENTRYPOINT ["/entrypoint.sh"]