from src.model_loader import load_model
import pandas as pd

model = load_model()

X_test = pd.read_parquet(
    "./notebooks/X_test_ml.parquet"
)

sample = X_test.iloc[[0]]

print("Type modèle :", type(model))

print("Prediction classe :", model.predict(sample))

print("Probabilité :", model.predict_proba(sample))

# Vérification que les colonnes sont bien compatibles
print(sample.shape)

print(len(model.feature_name_))

print(model.feature_name_[:10])

# Récupération du seuil métier
from mlflow import MlflowClient

client = MlflowClient()

model = client.get_model_version_by_alias(
    "P06_LightGBM_Optimized",
    "champion"
)

print(model.run_id)

run = client.get_run(
    model.run_id
)

print(
    run.data.metrics["best_threshold"]
)
