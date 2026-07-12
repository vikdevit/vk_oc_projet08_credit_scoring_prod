import mlflow
import pandas as pd

from mlflow.models import infer_signature
from mlflow.sklearn import load_model


mlflow.set_tracking_uri(
    "http://127.0.0.1:5000"
)


# -----------------------------
# Charger les données exemples
# -----------------------------
X = pd.read_parquet(
    "./notebooks/X_train_ml.parquet"
)

X_sample = X.head(5)


# -----------------------------
# Charger le modèle MLflow existant
# -----------------------------
model_uri = (
    "models:/P06_LightGBM_Optimized@champion"
)

model = mlflow.pyfunc.load_model(
    model_uri
)


# -----------------------------
# Générer une prédiction exemple
# -----------------------------
prediction = model.predict(
    X_sample
)


# -----------------------------
# Créer la signature
# -----------------------------
signature = infer_signature(
    X_sample,
    prediction
)


print(signature)
