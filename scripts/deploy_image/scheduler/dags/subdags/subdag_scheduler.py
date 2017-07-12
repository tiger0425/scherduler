# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from airflow.operators.python_operator import PythonOperator
from airflow import DAG
from tasks.log.config import logger
from tasks.worker.japan import refresh_4g_and_ready_ip, register
from tasks.ip import manage
from airflow.operators.dagrun_operator import TriggerDagRunOperator

def subdag_schedurler(parent_dag_name,child_dag_name,args,set_number):

    def op_get_ip(*args, **kwargs):
        logger.info('start the get ip')
        try:
            #ip = refresh_4g_and_ready_ip()
            ip = '192.168.1.1'
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

    def op_get_task(*args, **kwargs):
        # 从任务队列中获取任务
        # task = get_task()
        logger.info('start the get task')
        ip = kwargs['task_instance'].xcom_pull(task_ids='task_get_ip_%s' %(kwargs["params"]["cur_number"]))
        try:
            #task = get_task()
            task = 'register'
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
        ip = kwargs['task_instance'].xcom_pull(task_ids='task_get_ip_%s' %(kwargs["params"]["cur_number"]))
        logger.info('op_pass_ip get the ip and do pass the ip {}'.format(ip))

    def op_return_ip(*args, **kwargs):
        ip = kwargs['task_instance'].xcom_pull(task_ids='task_get_ip_%s' %(kwargs["params"]["cur_number"]))
        #manage.return_ip(ip, 'default')
        logger.info('return ip------{}'.format(kwargs["params"]["cur_number"]))

    def register_trigger(dag_run_obj,*args, **kwargs):
        ip = kwargs['task_instance'].xcom_pull(task_ids='task_get_ip_%s' %(kwargs["params"]["cur_number"]))
        task = kwargs['task_instance'].xcom_pull(task_ids='task_get_task_%s' %(kwargs["params"]["cur_number"]))
        if task=='register':
            logger.info('run register')
            dag_run_obj.payload = {'ip': ip}
            return dag_run_obj

    def shopcar_trigger(dag_run_obj,*args, **kwargs):
        ip = kwargs['task_instance'].xcom_pull(task_ids='task_get_ip_%s' %(kwargs["params"]["cur_number"]))
        task = kwargs['task_instance'].xcom_pull(task_ids='task_get_task_%s' %(kwargs["params"]["cur_number"]))
        if task=='shopcar':
            logger.info('run shopcar')
            dag_run_obj.payload = {'ip': ip}
            return dag_run_obj

    def wishlist_trigger(dag_run_obj,*args, **kwargs):
        ip = kwargs['task_instance'].xcom_pull(task_ids='task_get_ip_%s' %(kwargs["params"]["cur_number"]))
        task = kwargs['task_instance'].xcom_pull(task_ids='task_get_task_%s' %(kwargs["params"]["cur_number"]))
        if task=='wishlist':
            logger.info('run wishlist')
            dag_run_obj.payload = {'ip' : ip}
            return dag_run_obj

    dag_subdag = DAG(
        dag_id='%s.%s' % (parent_dag_name, child_dag_name),
        default_args=args,
        schedule_interval="@daily",
    )

    for i in range(set_number):
        task_get_ip = PythonOperator(
            task_id='task_get_ip_%s' %(i+1),
            provide_context=True,
            python_callable=op_get_ip,
            dag=dag_subdag)

        task_get_task = PythonOperator(
            task_id='task_get_task_%s' %(i+1),
            provide_context=True,
            python_callable=op_get_task,
            params={"cur_number": i+1},
            dag=dag_subdag)

        task_pass_ip = PythonOperator(
            task_id='task_pass_ip_%s' %(i+1),
            provide_context=True,
            python_callable=op_pass_ip,
            params={"cur_number": i + 1},
            depends_on_past=False,
            dag=dag_subdag)

        task_return_ip = PythonOperator(
            task_id='task_return_ip_%s' %(i+1),
            provide_context=True,
            python_callable=op_return_ip,
            params={"cur_number": i + 1},
            trigger_rule='one_success',
            depends_on_past=False,
            dag=dag_subdag)

        trigger_register = TriggerDagRunOperator(task_id='trigger_dag_register_%s' %(i+1),
                                                 trigger_dag_id="dag_register",
                                                 python_callable=register_trigger,
                                                 params={"cur_number": i + 1},
                                                 dag=dag_subdag)

        trigger_shopcar = TriggerDagRunOperator(task_id='trigger_dag_shopcar_%s' %(i+1),
                                                trigger_dag_id="dag_shopcar",
                                                python_callable=shopcar_trigger,
                                                params={"cur_number": i + 1},
                                                dag=dag_subdag)

        trigger_wishlist = TriggerDagRunOperator(task_id='trigger_dag_wishlist_%s' %(i+1),
                                                 trigger_dag_id="dag_wishlist",
                                                 python_callable=wishlist_trigger,
                                                 params={"cur_number": i + 1},
                                                 dag=dag_subdag)

        task_get_ip.set_downstream(task_pass_ip)
        task_get_ip.set_downstream(task_get_task)
        task_get_task.set_downstream(trigger_register)
        task_get_task.set_downstream(trigger_shopcar)
        task_get_task.set_downstream(trigger_wishlist)
        task_return_ip.set_upstream(trigger_register)
        task_return_ip.set_upstream(trigger_shopcar)
        task_return_ip.set_upstream(trigger_wishlist)

    return dag_subdag