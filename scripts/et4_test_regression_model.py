import joblib
import pandas as pd
import numpy as np

from src.model_loader import load_model
from src.model_config import load_threshold


# ==========================
# Chargement modèle v1
# ==========================

MODEL_PATH = "artifacts/model/model.joblib"

model_v1 = joblib.load(
    MODEL_PATH
)


# ==========================
# Chargement modèle v2
# ==========================

model_v2 = load_model()


# ==========================
# Chargement données test
# ==========================

X_test = pd.read_parquet(
    "data/X_test_ml.parquet"
)


# On prend un échantillon représentatif
X_sample = X_test.sample(
    n=1000,
    random_state=42
)


# ==========================
# Prédictions
# ==========================

proba_v1 = model_v1.predict_proba(
    X_sample
)[:,1]


proba_v2 = model_v2.predict_proba(
    X_sample
)[:,1]


# ==========================
# Comparaison scores
# ==========================

difference = np.abs(
    proba_v1 - proba_v2
)


print("==============================")
print("TEST NON REGRESSION MODELE")
print("==============================")


print(
    "Nombre prédictions comparées :",
    len(proba_v1)
)


print(
    "Différence maximale score :",
    difference.max()
)


print(
    "Différence moyenne score :",
    difference.mean()
)


# ==========================
# Comparaison décisions
# ==========================

threshold = load_threshold()


decision_v1 = (
    proba_v1 >= threshold
).astype(int)


decision_v2 = (
    proba_v2 >= threshold
).astype(int)


print(
    "Décisions identiques :",
    np.array_equal(
        decision_v1,
        decision_v2
    )
)


print(
    "Nombre décisions différentes :",
    np.sum(
        decision_v1 != decision_v2
    )
)
