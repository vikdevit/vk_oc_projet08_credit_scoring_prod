from fastapi import FastAPI

from app.schemas import (
    PredictionRequest,
    PredictionResponse
)

from app.predictor import predict


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
    request: PredictionRequest
):

    result = predict(
        request.features
    )

    return result
