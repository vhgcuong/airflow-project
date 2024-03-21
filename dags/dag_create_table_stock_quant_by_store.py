from datetime import timedelta, datetime
from airflow.models import DAG

from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

create_table_sql = '''
create table if not exists public.stock_quant_by_store ( 
id bigint not null,
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
    dag_id=f"run_query_create_table_v01",
    schedule_interval=None,
    default_args=default_args,
    start_date=datetime(2024, 3, 20, 0, 0, 0),
    tags=["cuongvh", "airflow_2.6"]
)

task1 = SQLExecuteQueryOperator(
    task_id='create_table',
    sql=create_table_sql,
    dag=dag,
    autocommit=True,
    conn_id='aws_redshift_conn',
    database='dev',
    show_return_value_in_logs=True
)

task1
