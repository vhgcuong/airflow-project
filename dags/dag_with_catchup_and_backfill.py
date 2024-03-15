from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'cuongvh',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
dag_id='dag_with_catchup_backfill_v02',
    default_args=default_args,
    start_date=datetime(2024, 3, 1),
    schedule="@daily",
    catchup=False,
    tags=["cuongvh", "airflow_2.6"],
) as dag:
    task1 = BashOperator(
        task_id='task1',
        bash_command="echo hello world, this is the first task!"
    )