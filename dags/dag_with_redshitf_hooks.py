from datetime import datetime, timedelta
from airflow.models import DAG

from airflow.providers.amazon.aws.operators.redshift_data import RedshiftDataOperator, RedshiftDataHook, RedshiftDataTrigger

default_args = {
    'owner': 'cuongvh',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id=f"example_dag_redshift_v01",
    schedule="@daily",
    default_args=default_args,
    start_date=datetime(2024, 3, 19),
    max_active_runs=1,
    catchup=False,
    tags=["cuongvh", "airflow_2.6"]
) as dag:
    task1 = RedshiftDataTrigger(
        aws_conn_id='aws_redshift'
    )

    task2 = RedshiftDataHook(

    )