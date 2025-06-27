from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import os
import logging

logger = logging.getLogger(__name__)

default_args = {
    'owner': 'zeus_nxtlvl',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

ZEUS_API_URL = os.getenv("ZEUS_API_URL", "http://zeus-api:8000")

def trigger_system_optimize():
    endpoint = f"{ZEUS_API_URL}/system/optimize"
    try:
        response = requests.post(endpoint)
        response.raise_for_status()
        logger.info("System optimization triggered")
    except requests.exceptions.RequestException as exc:
        logger.error(f"Failed to optimize system: {exc}")
        raise

def trigger_ai_model_training():
    endpoint = f"{ZEUS_API_URL}/ai/train_models"
    payload = {"model_type": "LSTMForecaster", "data_range": "daily_update", "gpu_accelerated": True}
    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        logger.info("AI model training triggered")
    except requests.exceptions.RequestException as exc:
        logger.error(f"Failed to train model: {exc}")
        raise

def trigger_strategy_generation():
    endpoint = f"{ZEUS_API_URL}/ai/generate_strategies"
    payload = {"analysis_period": "past_week_roi", "creativity_level": "high"}
    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        logger.info("Strategy generation triggered")
    except requests.exceptions.RequestException as exc:
        logger.error(f"Failed to generate strategies: {exc}")
        raise

with DAG(
    'zeus_ai_automation_dag',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=['zeus', 'ai', 'automation'],
) as dag:

    system_optimize_task = PythonOperator(
        task_id='system_optimization',
        python_callable=trigger_system_optimize
    )

    model_training_task = PythonOperator(
        task_id='ai_model_retraining',
        python_callable=trigger_ai_model_training
    )

    strategy_generation_task = PythonOperator(
        task_id='new_strategy_generation',
        python_callable=trigger_strategy_generation
    )

    [model_training_task, strategy_generation_task] >> system_optimize_task
