from fastapi import FastAPI

from . import routers

app = FastAPI(title="ZEUS NXTLVL")

app.include_router(routers.router)

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
