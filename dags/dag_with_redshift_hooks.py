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
            CREATE TABLE if not exists dev.stock_quant_by_store (
                id serial4 NOT NULL,
                product_code varchar NULL,
                store_code varchar NULL,
                qty float8 NULL,
                qty_updated bool NULL DEFAULT true,
                product_jan_1 varchar NULL,
                last_updated timestamp NULL,
                "level" int4 NULL,
                conversion_lvl_1_id int8 NULL,
                conversion_lvl_1_qty float8 NULL,
                to_lvl_1_qty float8 NULL,
                conversion_lvl_2_id int8 NULL,
                conversion_lvl_2_qty float8 NULL,
                to_lvl_2_qty float8 NULL,
                qty_pcs float8 NULL,
                qty_pcs_od float8 NULL,
                CONSTRAINT stock_quant_by_store_product_code_store_code_key UNIQUE (product_code, store_code)
            );
            CREATE UNIQUE INDEX product_store_idx ON public.stock_quant_by_store USING btree (product_code, store_code);
            CREATE INDEX stock_quant_by_store_conversion_lvl_1_id_idx ON public.stock_quant_by_store USING btree (conversion_lvl_1_id);
            CREATE INDEX stock_quant_by_store_conversion_lvl_2_id_idx ON public.stock_quant_by_store USING btree (conversion_lvl_2_id);
            CREATE INDEX stock_quant_by_store_id_idx ON public.stock_quant_by_store USING btree (id);
            CREATE INDEX stock_quant_by_store_level_idx ON public.stock_quant_by_store USING btree (level);
            CREATE INDEX stock_quant_by_store_product_code_idx ON public.stock_quant_by_store USING btree (product_code);
            CREATE INDEX stock_quant_by_store_store_code_idx ON public.stock_quant_by_store USING btree (store_code);
        ''',
        params={
            "schema": "dev",
            "table": "listing"
        }
    )
