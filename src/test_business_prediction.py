import pandas as pd

from src.model_loader import load_model
from mlflow import MlflowClient


# ------------------------
# Charger modèle
# ------------------------

model = load_model()


# ------------------------
# Charger données
# ------------------------

X_test = pd.read_parquet(
    "./notebooks/X_test_ml.parquet"
)


sample = X_test.iloc[[0]]


# ------------------------
# Probabilité
# ------------------------

proba = model.predict_proba(sample)[:, 1]


# ------------------------
# Charger seuil métier
# ------------------------

client = MlflowClient(
    tracking_uri="http://127.0.0.1:5000"
)


model_version = client.get_model_version_by_alias(
    "P06_LightGBM_Optimized",
    "champion"
)


run = client.get_run(
    model_version.run_id
)


threshold = run.data.metrics["best_threshold"]


# ------------------------
# Décision métier
# ------------------------

decision = int(proba[0] >= threshold)


# ------------------------
# Affichage utilisateur
# ------------------------

print("==========================")
print("Client :", int(sample["SK_ID_CURR"].iloc[0]))
print("Probabilité défaut :", round(float(proba[0]),4))
print("Seuil métier :", round(threshold,4))
print("Décision :", decision)
print("==========================")
