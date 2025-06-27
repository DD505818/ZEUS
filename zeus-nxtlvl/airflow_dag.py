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
    'start_date': datetime(2024, 1, 1), # Start date can be in the past
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Base URL for the ZEUS API (accessible via Docker Compose service name or actual IP in prod)
# This uses an environment variable, crucial for production deployments.
ZEUS_API_URL = os.getenv("ZEUS_API_URL", "http://zeus-api:8000")

def trigger_system_optimize():
    """Triggers the backend's system optimization process (e.g., GeminiTuner adjusting agent params)."""
    endpoint = f"{ZEUS_API_URL}/system/optimize"
    try:
        response = requests.post(endpoint)
        response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
        logger.info(f"System optimization triggered successfully: {response.json()}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to trigger system optimization from Airflow: {e}")
        raise # Re-raise to mark the Airflow task as failed

def trigger_ai_model_training():
    """Triggers the backend's AI model retraining process (e.g., for LSTMForecaster on GPU nodes)."""
    endpoint = f"{ZEUS_API_URL}/ai/train_models"
    payload = {
        "model_type": "LSTMForecaster",
        "data_range": "daily_update",
        "gpu_accelerated": True
    }
    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        logger.info(f"AI model training triggered successfully: {response.json()}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to trigger AI model training from Airflow: {e}")
        raise

def trigger_strategy_generation():
    """Triggers the backend's StrategyForge Engine (Gemini) for new strategy generation."""
    endpoint = f"{ZEUS_API_URL}/ai/generate_strategies"
    payload = {
        "analysis_period": "past_week_roi",
        "creativity_level": "high"
    }
    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        logger.info(f"Strategy generation triggered successfully: {response.json()}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to trigger strategy generation from Airflow: {e}")
        raise


with DAG('zeus_ai_automation_dag',
         default_args=default_args,
         schedule_interval='@daily', # This DAG will run once every day
         catchup=False, # Don't run for past missed schedules
         tags=['zeus', 'ai', 'automation']) as dag:

    # Task to trigger daily system optimization (e.g., GeminiTuner adjusts agent parameters)
    system_optimize_task = PythonOperator(
        task_id='system_optimization',
        python_callable=trigger_system_optimize
    )

    # Task to trigger AI model retraining (e.g., LSTMForecaster updates its predictive models)
    model_training_task = PythonOperator(
        task_id='ai_model_retraining',
        python_callable=trigger_ai_model_training
    )

    # Task to trigger new strategy generation (StrategyForge Engine proposes new strategies)
    strategy_generation_task = PythonOperator(
        task_id='new_strategy_generation',
        python_callable=trigger_strategy_generation
    )

    # Define task dependencies: model training and strategy generation can run in parallel,
    # and then the system optimization (which might use new models/strategies) follows.
    [model_training_task, strategy_generation_task] >> system_optimize_task
