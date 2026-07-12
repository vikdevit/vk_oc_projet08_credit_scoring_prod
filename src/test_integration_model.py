import pandas as pd

from src.model_loader import load_model
from src.model_config import load_threshold


def test_prediction():

    model = load_model()

    threshold = load_threshold()

    X_test = pd.read_parquet(
        "./notebooks/X_test_ml.parquet"
    )

    sample = X_test.iloc[[0]]

    probability = model.predict_proba(sample)[0,1]

    decision = int(probability >= threshold)

    assert probability >= 0
    assert probability <= 1
    assert decision in [0,1]

    print(
        probability,
        threshold,
        decision
    )


test_prediction()
