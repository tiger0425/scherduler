# coding:utf-8

import time
import datetime
from airflow.operators.python_operator import PythonOperator
from airflow import DAG
from tasks.log.config import logger
from tasks.worker.japan import refresh_4g_and_ready_ip, register
from tasks.ip import manage
from airflow.operators.dagrun_operator import TriggerDagRunOperator

args = {
    'owner': 'manager',
    'start_date': (datetime.datetime.now() - datetime.timedelta(minutes=15)),
    'depends_on_past': False,
}

def op_get_ip(*args, **kwargs):
    logger.info('start the get ip')
    try:
        ip = refresh_4g_and_ready_ip()
        return ip

    except Exception as e:
        message = e.message
        logger.error('=======get the error message=====')
        logger.error(e)
        if 'error' in message:
            ip = message.split(':')[-1]
            manage.return_ip(ip, 'default')
            # make sure always return the ip as require
            raise ValueError('finally return the ip and do stop the rest task ')


def op_get_task():
    #从任务队列中获取任务
    #task = get_task()
    logger.info('start the get task')
    ip = kwargs['task_instance'].xcom_pull(task_ids='task_get_ip')
    try:
        task = get_task()
        return task
    except Exception as e:
        message = e.message
        logger.error('=======get the error message=====')
        logger.error(e)
        if 'error' in message:
            ip = message.split(':')[-1]
            manage.return_ip(ip, 'default')
            # make sure always return the ip as require
            raise ValueError('finally return the ip and do stop the rest task ')


def op_pass_ip(*args, **kwargs):
    ip = kwargs['task_instance'].xcom_pull(task_ids='task_get_ip')
    logger.info('op_pass_ip get the ip and do pass the ip '.format(ip))


def op_return_ip(*args, **kwargs):
    ip = kwargs['task_instance'].xcom_pull(task_ids='task_get_ip')
    manage.return_ip(ip, 'default')

def register_trigger(*args, **kwargs,dag_run_obj):
    ip = kwargs['task_instance'].xcom_pull(task_ids='task_get_ip')
    task = kwargs['task_instance'].xcom_pull(task_ids='task_get_task')
    if task='register':
        logger.info('run register')
        return dag_run_obj

def register_shopcar(*args, **kwargs,dag_run_obj):
    ip = kwargs['task_instance'].xcom_pull(task_ids='task_get_ip')
    task = kwargs['task_instance'].xcom_pull(task_ids='task_get_task')
    if task='shopcar':
        logger.info('run shopcar')
        return dag_run_obj

def register_wishlist(*args, **kwargs,dag_run_obj):
    ip = kwargs['task_instance'].xcom_pull(task_ids='task_get_ip')
    task = kwargs['task_instance'].xcom_pull(task_ids='task_get_task')
    if task='wishlist':
        logger.info('run wishlist')
        return dag_run_obj

dag = DAG(
    dag_id='dag_scheduler',
    default_args=args,
    schedule_interval='*/5 * * * *')

task_get_ip = PythonOperator(
    task_id='task_get_ip',
    provide_context=True,
    python_callable=op_get_ip,
    dag=dag)

task_get_task = PythonOperator(
    task_id='task_get_task',
    provide_context=True,
    python_callable=op_get_task,
    dag=dag)


task_pass_ip = PythonOperator(
    task_id='task_pass_ip',
    provide_context=True,
    python_callable=op_pass_ip,
    depends_on_past=False,
    dag=dag)

task_return_ip = PythonOperator(
    task_id='task_return_ip',
    provide_context=True,
    python_callable=op_return_ip,
    trigger_rule='one_success',
    depends_on_past=False,
    dag=dag)

trigger_register = TriggerDagRunOperator(task_id='trigger_dag_register',
                                trigger_dag_id="dag_register",
                                python_callable=register_trigger,
                                dag=dag)

trigger_shopcar = TriggerDagRunOperator(task_id='trigger_dag_shopcar',
                                trigger_dag_id="dag_shopcar",
                                python_callable=shopcar_trigger,
                                dag=dag)

trigger_wishlist = TriggerDagRunOperator(task_id='trigger_dag_wishlist',
                                trigger_dag_id="dag_wishlist",
                                python_callable=wishlist_trigger,
                                dag=dag)

task_get_ip.set_downstream(task_pass_ip)
task_get_ip.set_downstream(task_get_task)
task_get_task.set_downstream(trigger_register )
task_get_task.set_downstream(trigger_shopcar  )
task_get_task.set_downstream(trigger_wishlist )

task_pass_ip >> task_return_ip
trigger_wishlist >> task_return_ip
trigger_shopcar >> task_return_ip
trigger_register >> task_return_ip