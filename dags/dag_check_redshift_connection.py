from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'cuongvh',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

def check_redshift_connection():
    try:
        redshift_hook = PostgresHook(postgres_conn_id='aws_redshift_conn')  # Replace 'redshift_conn_id' with your connection ID
        redshift_conn = redshift_hook.get_conn()
        redshift_conn.close()
        print("Redshift connection successful!")
    except Exception as e:
        print(f"Error connecting to Redshift: {str(e)}")

with DAG(
    'check_redshift_connection_v08',
    default_args=default_args,
    description='Check Redshift connection example',
    schedule='@daily',
    catchup=True,
    start_date=datetime(2024, 3, 19),
    tags=["cuongvh", "airflow_2.6"]
) as dag:

    check_connection_task = PythonOperator(
        task_id='check_redshift_connection',
        python_callable=check_redshift_connection,
        dag=dag
    )

    bash_vim = BashOperator(
        task_id='bash_vim',
        bash_command="vim --version"
    )

    check_connection_task >> bash_vim
