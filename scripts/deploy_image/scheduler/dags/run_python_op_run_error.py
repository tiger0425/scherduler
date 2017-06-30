from airflow.operators.python_operator import PythonOperator
from airflow import DAG
from airflow.utils import dates
import time
from tasks.config import logger

args = {
    'owner': 'airflow',
    'start_date': dates.days_ago(1),
    'depends_on_past': False,
    # 'pool': 1
}


def op_task_1(*args, **kwargs):
    print "i can sleep very good"
    time.sleep(5)
    return 'i pass the value to task_2'


def op_task_2(*args, **kwargs):
    print "op_print_hello"

    raise ValueError("i just throw an error here ")


def op_task_3(*args, **kwargs):
    value = kwargs['task_instance'].xcom_pull(task_ids='task_1')
    print value
    print "op_print_hello"
    logger.info('not i print the message {}'.format(str(time.time())))
    return 'hello'


def op_task_4(*args, **kwargs):
    value = kwargs['task_instance'].xcom_pull(task_ids='task_1')
    print value
    print "op_print_hello"
    logger.info('not i print the message {}'.format(str(time.time())))
    return 'hello'


dag = DAG(
    dag_id='run_python_op_run_error',
    default_args=args,
    schedule_interval='*/5 * * * *')

task_1 = PythonOperator(
    task_id='task_1',
    provide_context=True,
    python_callable=op_task_1,
    dag=dag)

task_2 = PythonOperator(
    task_id='task_2',
    provide_context=True,
    python_callable=op_task_2,
    depends_on_past=False,
    dag=dag)

task_3 = PythonOperator(
    task_id='task_3',
    provide_context=True,
    python_callable=op_task_3,
    depends_on_past=False,
    dag=dag)

task_4 = PythonOperator(
    task_id='task_4',
    provide_context=True,
    python_callable=op_task_4,
    trigger_rule='one_success',
    depends_on_past=False,
    dag=dag)

task_1.set_downstream(task_2)
task_1.set_downstream(task_3)
task_2 >> task_4
task_3 >> task_4
