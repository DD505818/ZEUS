# ZEUS NXTLVL

This repository contains a simplified prototype of an autonomous trading engine. It includes a set of lightweight trading indicators and a basic orchestration engine used for demonstration purposes.  The project is intentionally minimal and does not execute real trades.

## Running the demo

Install dependencies and launch the example script:

```bash
pip install -r requirements.txt
python main.py
```

The example repeatedly generates random price data and prints the decision returned by the trading engine.

## Tests

After installing requirements you can run the unit tests:

```bash
python -m unittest discover tests
```

## Docker demo

Build and launch the containers using docker compose:

```bash
docker-compose up --build
```

This starts a demo FastAPI service on port 3000 and an Airflow UI on port 8080.
