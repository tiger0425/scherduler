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

from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.subdag_operator import SubDagOperator
from subdags.subdag_scheduler import subdag_schedurler

DAG_NAME = 'dag_main'

args = {
    'owner': 'tiger',
    'start_date': (datetime.datetime.now() - datetime.timedelta(minutes=15)),
    #'depends_on_past': False,
}

dag = DAG(
    dag_id=DAG_Name,
    default_args=args,
    schedule_interval='*/5 * * * *')

SubDagOperator(
    task_id='scheduler',
    subdag=subdag_schedurler(DAG_NAME, 'scheduler', args, 10),
    default_args=args,
    dag=dag,
)