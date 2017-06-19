FROM puckel/docker-airflow:1.8.1

COPY ./requirements.txt /usr/local/airflow/requirements.txt
RUN mkdir -p /scheduler/log
RUN pip install --user -r requirements.txt