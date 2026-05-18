from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'mci_engineer',
    'start_date': datetime(2026, 5, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

with DAG(
    'orders_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    max_active_runs=1,
    description='Orders API Pipeline'
) as dag:

    ingest_orders = BashOperator(
        task_id='fetch_orders',
        bash_command='python /opt/airflow/dags/scripts/fetch_orders.py'
    )

    process_orders = BashOperator(
        task_id='process_orders',
        bash_command='python /opt/airflow/dags/scripts/process_orders.py'
    )

    ingest_orders >> process_orders