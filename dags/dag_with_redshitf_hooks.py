from datetime import datetime, timedelta
from airflow.models import DAG

from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator

create_table_sql = '''
create table if not exists public.stock_quant_by_store ( id bigint not null,
product_code varchar null,
store_code varchar null,
qty float8 null,
qty_updated bool null default true,
product_jan_1 varchar null,
last_updated TIMESTAMP null,
"level" int4 null,
conversion_lvl_1_id int8 null,
conversion_lvl_1_qty float8 null,
to_lvl_1_qty float8 null,
conversion_lvl_2_id int8 null,
conversion_lvl_2_qty float8 null,
to_lvl_2_qty float8 null,
qty_pcs float8 null,
qty_pcs_od float8 null,
constraint stock_quant_by_store_product_code_store_code_key unique (product_code,
store_code) );
'''

default_args = {
    'owner': 'cuongvh',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    dag_id=f"run_query_in_redshift_v13",
    schedule="@daily",
    default_args=default_args,
    start_date=datetime(2024, 3, 20, 0, 0, 0),
    max_active_runs=1,
    catchup=True,
    tags=["cuongvh", "airflow_2.6"]
)

def execute_redshift_query_and_display_result(**kwargs):
    # Define your SQL query
    sql_query = "SELECT * FROM public.stock_quant_by_store;"

    # Create a PostgresHook to execute the query
    redshift_hook = PostgresHook(postgres_conn_id='redshift_conn_id')  # Replace 'redshift_conn_id' with your connection ID
    connection = redshift_hook.get_conn()
    cursor = connection.cursor()

    # Execute the query
    cursor.execute(sql_query)

    # Fetch and display the result
    result = cursor.fetchall()
    print("Query result:")
    print(result)

    # Close cursor and connection
    cursor.close()
    connection.close()

def execute_insert_query():
    sql_query = """
        
    """

    redshift_hook = PostgresHook(postgres_conn_id='redshift_conn_id')  # Replace 'redshift_conn_id' with your connection ID
    connection = redshift_hook.get_conn()
    cursor = connection.cursor()

    # Execute the query
    cursor.execute(sql_query)

    # Close cursor and connection
    cursor.close()
    connection.close()

task1 = SQLExecuteQueryOperator(
        task_id='create_table',
        sql=create_table_sql,
        dag=dag,
        autocommit=True,
        conn_id='aws_redshift_conn',
        database='dev',
        show_return_value_in_logs=True
    )

task2 = PythonOperator(
    task_id='execute_redshift_query_and_display_result',
    python_callable=execute_redshift_query_and_display_result,
    provide_context=True,
    dag=dag
)

task1 >> task2
