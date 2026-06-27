from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from main_bigquery import main_bigquery


# Default task settings
default_args = {
    "owner": "adam",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


# Define DAG
with DAG(
    dag_id="bmkg_bigquery_etl",
    default_args=default_args,
    description="BMKG Earthquake ETL Pipeline to BigQuery (Hybrid GCP)",
    schedule_interval="0 */8 * * *",  # every 8 hours
    start_date=datetime(2026, 5, 17),
    catchup=False,
    tags=["bmkg", "bigquery", "gcp", "etl", "data-engineering"],
) as dag:

    # Main ETL Task
    run_bigquery_etl = PythonOperator(
        task_id="run_bigquery_etl_pipeline",
        python_callable=main_bigquery,
    )

    run_bigquery_etl