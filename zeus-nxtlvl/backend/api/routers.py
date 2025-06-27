from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ModelTrainRequest(BaseModel):
    model_type: str
    data_range: str
    gpu_accelerated: bool = False


class StrategyRequest(BaseModel):
    analysis_period: str
    creativity_level: str

@router.post("/system/optimize")
async def system_optimize() -> dict:
    return {"message": "system optimize triggered"}

@router.post("/ai/train_models")
async def ai_train_models(payload: ModelTrainRequest) -> dict:
    return {"message": "ai model training triggered", "payload": payload.dict()}

@router.post("/ai/generate_strategies")
async def generate_strategies(payload: StrategyRequest) -> dict:
    return {"message": "strategy generation triggered", "payload": payload.dict()}
