from fastapi import FastAPI
from prometheus_client import Summary, make_asgi_app
import os

app = FastAPI()
REQUEST_TIME = Summary('zeus_request_processing_seconds', 'Time spent processing request')

@app.on_event('startup')
async def startup_event() -> None:
    app.mount('/metrics', make_asgi_app())

@app.get('/health')
async def health() -> dict:
    return {"status": "exporter alive"}
