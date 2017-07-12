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

from airflow.operators.python_operator import PythonOperator
from airflow.models import DAG
from datetime import datetime
from tasks.log.config import logger

args = {
    'owner': 'tiger',
    'start_date': (datetime.datetime.now() - datetime.timedelta(minutes=15)),
    #'depends_on_past': False,
}

dag = DAG(
    dag_id='dag_shopcar',
    default_args=args,
    schedule_interval=None)

def op_shopcar(*args, **kwargs):
    logger.info('register run IP {}'.format(kwargs['dag_run'].conf['ip']))

task_register = PythonOperator(
    task_id='task_shopcar',
    provide_context=True,
    python_callable=op_shopcar,
    depends_on_past=False,
    dag=dag)