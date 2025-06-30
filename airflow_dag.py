from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from zeus_trade_engine import ZeusTradeEngine

default_args = {
    'owner': 'zeus_nxtlvl',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


def run_zeus_wrapper() -> None:
    engine = ZeusTradeEngine()
    payload_prices = [100, 101, 103]
    payload_orderbook = {'bid_volume': 500, 'ask_volume': 100}
    result = engine.run(payload_prices, payload_orderbook)
    print(f"Trade Executed: {result}")


with DAG(
    'zeus_ai_trading_dag',
    default_args=default_args,
    schedule_interval='@hourly',
    catchup=False,
) as dag:
    run_task = PythonOperator(
        task_id='run_zeus_engine',
        python_callable=run_zeus_wrapper,
    )
