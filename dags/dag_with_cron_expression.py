from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'cuongvh',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='dag_with_cron_expression_v05',
    default_args=default_args,
    start_date=datetime(2024, 3, 1),
    schedule='0 4 * * Mon-Fri',
    tags=["cuongvh", "airflow_2.6"],
) as dag:
    task1 = BashOperator(
        task_id='task1',
        bash_command="echo dag with cron expression"
    )