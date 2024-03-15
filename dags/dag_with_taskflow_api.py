from datetime import datetime, timedelta

from airflow.decorators import dag, task

default_args = {
    'owner': 'cuongvh',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

@dag(dag_id='dag_with_taskflow_api_v03',
     default_args=default_args,
     start_date=datetime(2024, 3, 1),
     schedule='@daily',
     tags=["cuongvh", "airflow_2.6"])
def hello_world_etl():

    @task(multiple_outputs=True)
    def get_name():
        return {
            'first_name': 'Cuong',
            'last_name': 'Vu Hung'
        }

    @task()
    def get_age():
        return 29

    @task()
    def greet(first_name, last_name, age):
        print(f"Xin chao! Toi la {first_name} {last_name} "
              f"va toi {age} tuoi!")

    name_dict = get_name()
    age = get_age()
    greet(first_name=name_dict['first_name'],
          last_name=name_dict['last_name'],
          age=age)

greet_dag = hello_world_etl()
