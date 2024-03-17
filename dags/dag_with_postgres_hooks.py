from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'cuongvh',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

def postgres_to_s3():
    # step 1: query data from postgresql db and save into text file
    pass

    # step 2: upload text file into s3
    pass

with DAG(
    dag_id='dag_with_postgres_hooks_v05',
    default_args=default_args,
    start_date=datetime(2024, 3, 1),
    schedule='0 4 * * *',
    tags=["cuongvh", "airflow_2.6"],
) as dag:
    pass