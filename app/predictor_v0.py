import pandas as pd

from sqlalchemy.orm import Session

from src.model_loader import load_model
from src.model_config import load_threshold

from app.models.models import Prediction, InputData

#def predict(features):
#
#    model = load_model()
#
#    threshold = load_threshold()
#
#
#    df = pd.DataFrame(
#        [features]
#    )
#
#
#    probability = model.predict_proba(
#        df
#    )[0][1]
#
#
#    decision = int(
#        probability >= threshold
#    )
#
#
#    return {
#        "client_id": int(
#            df["SK_ID_CURR"].iloc[0]
#        ),
#        "probability_default": float(
#            probability
#        ),
#        "threshold": float(
#            threshold
#        ),
#        "decision": decision
#    }

def predict(features, db: Session):

    model = load_model()

    threshold = load_threshold()


    df = pd.DataFrame(
        [features]
    )


    probability = model.predict_proba(
        df
    )[0][1]


    decision = int(
        probability >= threshold
    )


    client_id = int(
        df["SK_ID_CURR"].iloc[0]
    )


    # ==========================
    # Sauvegarde input
    # ==========================

    input_record = InputData(
        client_id=client_id,
        features=features
    )

    db.add(input_record)


    # ==========================
    # Sauvegarde prédiction
    # ==========================

    prediction_record = Prediction(
        client_id=client_id,
        prediction=decision,
        score=float(probability),
        threshold=float(threshold)
    )

    db.add(prediction_record)


    db.commit()


    return {
        "client_id": client_id,
        "probability_default": float(probability),
        "threshold": float(threshold),
        "decision": decision
    }
Étape 7.2.3 —
