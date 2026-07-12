from pydantic import BaseModel
from typing import Dict, Any


class PredictionRequest(BaseModel):

    features: Dict[str, Any]


class PredictionResponse(BaseModel):

    client_id: int
    probability_default: float
    threshold: float
    decision: int
