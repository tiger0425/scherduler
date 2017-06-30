# -*- coding: utf-8 -*-
from airflow.operators.python_operator import PythonOperator
from airflow import DAG

from airflow.utils import dates
import time
from tasks import task_web_driver

args = {
    'owner': 'airflow',
    'start_date': dates.days_ago(1),
    'depends_on_past': False,
    # 'pool': 1
}


def sleep_func(*args, **kwargs):
    print "i can sleep very good"
    time.sleep(5)


dag = DAG(
    dag_id='run_python_dag', default_args=args,
    schedule_interval='*/5 * * * *')

task_get_blogs = PythonOperator(
    task_id='task_get_blogs',
    # provide_context=True,
    python_callable=task_web_driver.get_cnblogs,
    dag=dag)

task_sleep_this = PythonOperator(
    task_id='sleep_this',
    # provide_context=True,
    python_callable=sleep_func,
    dag=dag)

task_sleep_this.set_upstream(task_get_blogs)
