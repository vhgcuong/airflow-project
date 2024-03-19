from datetime import datetime
from airflow.models import DAG
from airflow.providers.amazon.aws.operators.redshift_sql import RedshiftSQLOperator

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

    t = RedshiftSQLOperator(
        task_id='stock_quant_by_store_v01',
        sql='''
            
        ''',
        params={
            "schema": "dev",
            "table": "..."
        }
    )
