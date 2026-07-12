import pandas as pd

from src.model_loader import load_model
from src.model_config import load_threshold


model = load_model()

threshold = load_threshold()


def predict(features):

    df = pd.DataFrame(
        [features]
    )

    probability = model.predict_proba(
        df
    )[0][1]


    decision = int(
        probability >= threshold
    )


    return {
        "client_id": int(
            df["SK_ID_CURR"].iloc[0]
        ),
        "probability_default": float(
            probability
        ),
        "threshold": float(
            threshold
        ),
        "decision": decision
    }
