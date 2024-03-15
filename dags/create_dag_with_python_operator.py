from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'cuongvh',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

def greet(ti):
    first_name = ti.xcom_pull(task_ids='get_name', key='first_name')
    last_name = ti.xcom_pull(task_ids='get_name', key='last_name')
    
    age = ti.xcom_pull(task_ids='get_age', key='age')
    
    print(f"Hello World! My name is {first_name} {last_name}, "
          f"and I am {age} years old!")


def get_name(ti):
    ti.xcom_push(key='first_name', value='Cuong')
    ti.xcom_push(key='last_name', value='Vu Hung')

def get_age(ti):
    ti.xcom_push(key='age', value=29)

with DAG(
    dag_id='our_dag_with_python_operator_v06',
    default_args=default_args,
    description='Our first dag using python operator',
    start_date=datetime(2024, 3, 14),
    schedule="2 * * * *",
    catchup=True,
    tags=["cuongvh", "airflow_2.6"],
) as dag:
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet,
        op_kwargs={'age': 25}
    )

    task2 = PythonOperator(
        task_id='get_name',
        python_callable=get_name
    )
    
    task3 = PythonOperator(
        task_id='get_age',
        python_callable=get_age
    )

    [task2, task3] >> task1