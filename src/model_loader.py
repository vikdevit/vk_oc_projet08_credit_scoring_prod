import joblib
from pathlib import Path


MODEL_PATH = Path(
    "artifacts/model/model.joblib"
)


def load_model():

    return joblib.load(
        MODEL_PATH
    )
