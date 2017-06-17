from airflow.operators.python_operator import PythonOperator
from airflow import DAG
from airflow.utils import dates
import time
from tasks import task_web_driver

args = {
    'owner': 'airflow',
    'start_date': dates.days_ago(1),
    'depends_on_past': False,
}


def sleep_func():
    print "i can sleep very good"
    time.sleep(5)


dag = DAG(
    dag_id='python_operator', default_args=args,
    schedule_interval='*/5 * * * *')

get_cnblogs = PythonOperator(
    task_id='get_cnblogs',
    provide_context=True,
    python_callable=task_web_driver.get_cnblogs,
    dag=dag)

sleep_this = PythonOperator(
    task_id='sleep_this',
    provide_context=True,
    python_callable=sleep_func,
    dag=dag)


sleep_this.set_upstream(get_cnblogs)
