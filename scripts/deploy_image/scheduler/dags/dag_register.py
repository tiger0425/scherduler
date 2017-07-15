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
import airflow
import datetime
import time
from tasks.ip import manage
from airflow.operators.python_operator import PythonOperator
from airflow.models import DAG
from tasks.log.config import logger

args = {
    'owner': 'register',
    'start_date': (datetime.datetime.now() - datetime.timedelta(minutes=1)),
    'depends_on_past': False,
}

dag = DAG(
    dag_id='dag_register',
    default_args=args,
    schedule_interval=None)

def op_register(*args, **kwargs):
    ip = kwargs['dag_run'].conf['ip']
    taskid  = kwargs['dag_run'].conf['taskid']
    host = kwargs['dag_run'].conf['host']
    #time.sleep(300)
    logger.info('taskid ---- {}'.format(taskid))
    logger.info('host ---- {}'.format(host))
    logger.info('register run IP {}'.format(ip))
    manage.return_ip(ip, 'default')
    #logger.info('return ip------{}'.format(ip))



task_register = PythonOperator(
    task_id='task_register',
    provide_context=True,
    python_callable=op_register,
    depends_on_past=False,
    dag=dag)