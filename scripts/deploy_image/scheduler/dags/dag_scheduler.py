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

import random
import time
import json
import datetime
from airflow.operators.python_operator import PythonOperator
from airflow import DAG
from tasks.log.config import logger
import commands


from tasks.settings import IP_PROXY_SERVER, DIAL_TIME_OUT
import requests
from urlparse import urljoin

args = {
    'owner': 'tiger',
    'start_date': (datetime.datetime.now() - datetime.timedelta(minutes=2)),
    'depends_on_past': False,
}

dag = DAG(
    dag_id='dag_scheduler',
    default_args=args,
    schedule_interval='@once')





def op_scheduler(*args, **kwargs):
    tag = 'default'

    while True:
        #获取有用的IP,如果没有就等待
        logger.info('start the get ip')
        url = urljoin(IP_PROXY_SERVER, '/api/ip/get')
        data = {
            'direct': 'left',
            'tag': tag,
        }
        ip = requests.post(url=url, data=data).json()

        if not ip:
            time.sleep(5)
            continue

        # {"result":"192.168.1.3:8888","status":200}
        result = ip.get('result', '')
        if not result:
            time.sleep(5)
            continue

        # 从任务队列中获取任务
        # task = get_task()

        logger.info('start the get task')
        url = urljoin('http://192.168.1.251:9001', '/api/task/get')
        #task_json = requests.post(url=url, data=data).json()
        r = requests.get(url=url)
        dirc = json.loads(r.text)
        task_result = eval(dirc["result"])
        task = task_result["type"]
        task_id = task_result["tid"]
        task_host = task_result["host"]

        #task = get_task()
        #task = random.choice(['wishlist', 'register', 'shopcar'])


        if task == 'register':
            status, output = commands.getstatusoutput("airflow trigger_dag -c '{\"ip\":\"" + result + "\",\"taskid\":\"" + task_id +"\",\"host\":\"" + task_host +"\"}' dag_register")
        if task == 'wishlist':
            status, output = commands.getstatusoutput("airflow trigger_dag -c '{\"ip\":\"" + result + "\",\"taskid\":\"" + task_id +"\",\"host\":\"" + task_host +"\"}' dag_wishlist")
        elif task == 'shoppingcart':
            status, output = commands.getstatusoutput("airflow trigger_dag -c '{\"ip\":\"" + result + "\",\"taskid\":\"" + task_id +"\",\"host\":\"" + task_host +"\"}' dag_shopcar")

        logger.info(output)
        time.sleep(5)

for i in range(5):
    task_scheduler = PythonOperator(
                                    task_id='task_scheduler_%s' % (i+1),
                                    provide_context=True,
                                    python_callable=op_scheduler,
                                    depends_on_past=False,
                                    dag=dag)

