import csv
import os.path
from datetime import datetime, timedelta
from airflow.models import DAG

from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'cuongvh',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    dag_id=f"run_query_in_redshift_v02",
    schedule="@daily",
    default_args=default_args,
    start_date=datetime(2024, 3, 20, 0, 0, 0),
    tags=["cuongvh", "airflow_2.6"]
)

def execute_redshift_query_and_display_result(**kwargs):
    # Define your SQL query
    sql_query = "SELECT * FROM public.stock_quant_by_store;"

    # Create a PostgresHook to execute the query
    redshift_hook = PostgresHook(postgres_conn_id='aws_redshift_conn')  # Replace 'redshift_conn_id' with your connection ID
    connection = redshift_hook.get_conn()
    cursor = connection.cursor()

    # Execute the query
    cursor.execute(sql_query)

    # Fetch and display the result
    result = cursor.fetchall()

    file_name = './tmp/stock.csv'
    mode = 'a' if os.path.exists(file_name) else 'w'
    with open(file_name, mode, newline='') as file:
        writer = csv.writer(file)
        if mode == 'w':
            writer.writerow([
                'id',
                'product_code',
                'store_code',
                'qty',
                'qty_updated',
                'product_jan_1',
                'last_updated',
                'level',
                'conversion_lvl_1_id',
                'conversion_lvl_1_qty',
                'to_lvl_1_qty',
                'conversion_lvl_2_id',
                'conversion_lvl_2_qty',
                'to_lvl_2_qty',
                'qty_pcs',
                'qty_pcs_od'
            ])
        writer.writerows(result)

    # Close cursor and connection
    cursor.close()
    connection.close()

task2 = PythonOperator(
    task_id='execute_redshift_query_and_display_result',
    python_callable=execute_redshift_query_and_display_result,
    provide_context=True,
    dag=dag
)

task2
