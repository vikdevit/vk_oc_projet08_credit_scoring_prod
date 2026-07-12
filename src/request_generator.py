import pandas as pd
import json
import mlflow.sklearn

from mlflow import MlflowClient


# =========================
# CONFIGURATION
# =========================

MODEL_URI = "models:/P06_LightGBM_Optimized@champion"

DATA_PATH = "./notebooks/X_test_ml.parquet"


# =========================
# LOAD MODEL
# =========================

mlflow.set_tracking_uri(
    "http://127.0.0.1:5000"
)

model = mlflow.sklearn.load_model(
    MODEL_URI
)


# =========================
# LOAD THRESHOLD METIER
# =========================

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


print("Threshold métier :", threshold)


# =========================
# LOAD DATA
# =========================

X_test = pd.read_parquet(
    DATA_PATH
)


print("Shape X_test :", X_test.shape)


# =========================
# PREDICTIONS
# =========================

probabilities = model.predict_proba(
    X_test
)[:, 1]


decisions = (
    probabilities >= threshold
).astype(int)


X_test_copy = X_test.copy()

X_test_copy["probability_default"] = probabilities
X_test_copy["decision"] = decisions


# =========================
# CLIENT ACCEPTÉ (0)
# =========================

client_ok = X_test_copy[
    X_test_copy["decision"] == 0
].iloc[0]


# =========================
# CLIENT RISQUE (1)
# =========================

client_risk = X_test_copy[
    X_test_copy["decision"] == 1
].iloc[0]


# =========================
# EXPORT JSON
# =========================

def export_request(row, filename):

    data = row.drop(
        [
            "probability_default",
            "decision"
        ]
    ).to_dict()

    with open(
        filename,
        "w"
    ) as f:
        json.dump(
            data,
            f,
            indent=4
        )


export_request(
    client_ok,
    "./data/sample_request_client_ok.json"
)


export_request(
    client_risk,
    "./data/sample_request_client_risk.json"
)


# =========================
# DISPLAY DEMO INFO
# =========================

print("==============================")
print("CLIENT ACCEPTÉ")
print("==============================")
print(
    "SK_ID_CURR :",
    client_ok["SK_ID_CURR"]
)
print(
    "Probabilité défaut :",
    round(client_ok["probability_default"], 4)
)
print(
    "Décision :",
    client_ok["decision"]
)


print("==============================")
print("CLIENT RISQUE")
print("==============================")
print(
    "SK_ID_CURR :",
    client_risk["SK_ID_CURR"]
)
print(
    "Probabilité défaut :",
    round(client_risk["probability_default"], 4)
)
print(
    "Décision :",
    client_risk["decision"]
)
