from airflow.operators.python_operator import PythonOperator
from airflow import DAG
from airflow.utils import dates
import time
from tasks.config import logger

args = {
    'owner': 'airflow',
    'start_date': dates.days_ago(1),
    'depends_on_past': False,
    #'pool': 1
}


def op_sleep_func(*args, **kwargs):
    print "i can sleep very good"
    time.sleep(5)


def op_print_hello(*args, **kwargs):
    print "op_print_hello"
    return 'hello'


dag = DAG(
    dag_id='test_python_operator', default_args=args,
    schedule_interval='*/5 * * * *')

print_hello = PythonOperator(
    task_id='print_hello',
    provide_context=True,
    python_callable=op_print_hello,
    dag=dag)

sleep_this = PythonOperator(
    task_id='sleep_this',
    provide_context=True,
    python_callable=op_sleep_func,
    dag=dag)

sleep_this.set_upstream(print_hello)
