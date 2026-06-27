from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from main import main


def run_etl():
    main()


with DAG(
    dag_id="earthquake_etl",
    start_date=datetime(2026, 5, 10),
    schedule="0 */8 * * *",
    catchup=False,
    tags=["bmkg", "etl", "portfolio"]
) as dag:

    run_task = PythonOperator(
        task_id="run_etl_pipeline",
        python_callable=run_etl
    )