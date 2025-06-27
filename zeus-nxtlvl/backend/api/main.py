from fastapi import FastAPI
from .routers import router
from ..core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
