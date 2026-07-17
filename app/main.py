import time
import psutil

from fastapi import FastAPI, Depends

from sqlalchemy.orm import Session

from app.predictor import predict

from app.schemas import (
    PredictionRequest,
    PredictionResponse
)

from app.database.session import get_db

from app.models.api_log import ApiLog
from app.models.system_health_log import SystemHealthLog


app = FastAPI(
    title="Credit Scoring API",
    version="1.0"
)


@app.get("/")
def root():

    return {
        "message": "Credit Scoring API running"
    }


@app.get("/health")
def health():

    return {
        "status": "ok"
    }


@app.post(
    "/predict",
    response_model=PredictionResponse
)
def prediction(
    request: PredictionRequest,
    db: Session = Depends(get_db)
):

    # ==========================
    # Début mesure temps API
    # ==========================

    start_time = time.perf_counter()


    # ==========================
    # Appel modèle
    # ==========================

    result = predict(
        request.features,
        db
    )


    # ==========================
    # Calcul temps réponse
    # ==========================

    response_time = (
        time.perf_counter() - start_time
    ) * 1000


    # ==========================
    # Log appel API
    # ==========================

    api_log = ApiLog(
        endpoint="/predict",
        status_code=200,
        response_time=round(response_time, 2)
    )

    db.add(api_log)


    # ==========================
    # Log santé système
    # ==========================

    health_log = SystemHealthLog(
    cpu_usage=round(psutil.cpu_percent(), 2),
    memory_usage=round(psutil.virtual_memory().percent, 2),
    response_time=round(response_time, 2)
    )

    db.add(health_log)


    db.commit()


    return result
