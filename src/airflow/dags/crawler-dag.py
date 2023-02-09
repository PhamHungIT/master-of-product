from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import timedelta
import pendulum

default_args = {
    'owner': 'airflow',
    'retries':5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='crawler-dag',
    description='Get ticker list',
    start_date=pendulum.now(),
    schedule_interval='0 0 * * *',
    catchup=True
) as dag:
    dmx_crawler = BashOperator(
        task_id="dmx_crawler",
        bash_command='python3 ../crawler/dmx.py',
    )

    phongvu_crawler = BashOperator(
        task_id="phongvu_crawler",
        bash_command='python3 ../crawler/phongvu.py',
    )

    [dmx_crawler, phongvu_crawler]