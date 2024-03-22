import csv
import os.path
from itertools import groupby
from datetime import datetime, timedelta
from airflow.models import DAG

from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'cuongvh',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

query_stock_quant_by_store="SELECT store_code, qty FROM public.stock_quant_by_store;"
query_create_table_store_product_counts='''
create table if not exists public.store_product_counts ( 
id bigint not null,
store_code varchar null,
qty float8 null
'''

def execute_query_stock_quant_by_store(ds_nodash):
    redshift_hook = PostgresHook(postgres_conn_id='aws_redshift_conn')
    connection = redshift_hook.get_conn()
    cursor = connection.cursor()

    cursor.execute(query_stock_quant_by_store)

    result = cursor.fetchall()

    for item in result:
        pass

    file_name = f'./tmp/stock_{ds_nodash}.csv'
    mode = 'a' if os.path.exists(file_name) else 'w'
    with open(file_name, mode, newline='') as file:
        writer = csv.writer(file)
        if mode == 'w':
            writer.writerow([
                'store_code',
                'qty'
            ])
        writer.writerows(result)

    cursor.close()
    connection.close()

dag = DAG(
    dag_id=f"stock_quant_by_store_in_redshift_v02",
    schedule="@daily",
    default_args=default_args,
    start_date=datetime(2024, 3, 21),
    tags=["cuongvh", "airflow_2.6"]
)

task1 = PythonOperator(
    task_id='write_data_in_csv',
    python_callable=execute_query_stock_quant_by_store,
    provide_context=True,
    dag=dag
)

task1



