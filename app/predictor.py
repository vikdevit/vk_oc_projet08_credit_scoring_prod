import time

import pandas as pd
from sqlalchemy.orm import Session

from src.model_loader import load_model
from src.model_config import load_threshold

from app.models.prediction import Prediction
from app.models.input_data import InputData



MODEL_VERSION = "LightGBM_v1"


def predict(features: dict, db: Session):

    start_time = time.perf_counter()

    model = load_model()

    threshold = load_threshold()

    df = pd.DataFrame([features])

    probability = model.predict_proba(df)[0][1]

    decision = int(probability >= threshold)

    latency_ms = (
        time.perf_counter() - start_time
    ) * 1000

    client_id = int(
        df["SK_ID_CURR"].iloc[0]
    )

    # ==========================
    # Sauvegarde des données d'entrée
    # ==========================

    input_record = InputData(
        client_id=client_id,
        features=features
    )

    db.add(input_record)

    # ==========================
    # Sauvegarde de la prédiction
    # ==========================

    prediction_record = Prediction(
        client_id=client_id,
        prediction=decision,
        score=float(probability),
        threshold=float(threshold),
        model_version=MODEL_VERSION,
        latency_ms=float(latency_ms)
    )

    db.add(prediction_record)


    #db.commit()

    return {
        "client_id": client_id,
        "probability_default": float(probability),
        "threshold": float(threshold),
        "decision": decision
    }
