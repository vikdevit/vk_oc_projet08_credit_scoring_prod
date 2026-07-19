import time

import pandas as pd
import requests

from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed
)


# ==========================
# Configuration
# ==========================

API_URL = "https://vk-oc-projet08-credit-scoring-prod.onrender.com/predict"

DATA_PATH = "data/X_test_ml.parquet"

START_ROW = 16000

N_ROWS = 5000

MAX_WORKERS = 20


# ==========================
# Chargement données test
# ==========================

print("Chargement X_test...")

df = pd.read_parquet(DATA_PATH)

print(
    f"{len(df)} lignes disponibles"
)


# ==========================
# Sélection du lot
# ==========================

sample = df.iloc[
    START_ROW:START_ROW + N_ROWS
]

print(
    f"Simulation des lignes "
    f"{START_ROW} à "
    f"{START_ROW + len(sample) - 1}"
)

print(
    f"{len(sample)} prédictions"
)


# ==========================
# Fonction appel API
# ==========================

def call_api(row):

    payload = {
        "features": row.to_dict()
    }

    try:

        response = requests.post(
            API_URL,
            json=payload,
            timeout=60
        )

        if response.status_code == 200:

            return {
                "status": "OK"
            }

        else:

            return {
                "status": "ERROR",
                "code": response.status_code
            }

    except Exception as e:

        return {
            "status": "EXCEPTION",
            "error": str(e)
        }


# ==========================
# Simulation production
# ==========================

success = 0
errors = 0

start = time.time()

print(
    "Début simulation production..."
)

with ThreadPoolExecutor(
    max_workers=MAX_WORKERS
) as executor:

    futures = [

        executor.submit(
            call_api,
            row
        )

        for _, row in sample.iterrows()

    ]

    for future in as_completed(futures):

        result = future.result()

        if result["status"] == "OK":

            success += 1

        else:

            errors += 1

            print(result)


duration = time.time() - start


# ==========================
# Résultats
# ==========================

print("===================")

print("Simulation terminée")

print(
    "Succès :",
    success
)

print(
    "Erreurs :",
    errors
)

print(
    "Temps total :",
    round(duration, 2),
    "secondes"
)

print(
    "Débit :",
    round(success / duration, 2),
    "requêtes/sec"
)

print("===================")
