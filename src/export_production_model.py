import mlflow
import mlflow.sklearn
import joblib
import json
import os

from src.model_config import load_threshold


# Connexion MLflow
mlflow.set_tracking_uri(
    "http://127.0.0.1:5000"
)


# Charger le modèle Champion
model = mlflow.sklearn.load_model(
    "models:/P06_LightGBM_Optimized@champion"
)


# Créer le dossier cible
os.makedirs(
    "artifacts/model",
    exist_ok=True
)


# Export modèle
joblib.dump(
    model,
    "artifacts/model/model.joblib"
)


# Export seuil métier
threshold = load_threshold()

with open(
    "artifacts/model/threshold.json",
    "w"
) as f:
    json.dump(
        {
            "threshold": threshold
        },
        f,
        indent=4
    )


print("Modèle exporté_OK")
print("Seuil exporté_OK")
print("Threshold :", threshold)
