import pandas as pd
import requests
import time

from concurrent.futures import ThreadPoolExecutor, as_completed


# ==========================
# Configuration
# ==========================

API_URL = "https://vk-oc-projet08-credit-scoring-prod.onrender.com/predict"

DATA_PATH = "data/X_test_ml.parquet"

N_ROWS = 48744

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
# Sélection échantillon
# ==========================

sample = df.head(N_ROWS)


print(
    f"Simulation de {len(sample)} prédictions"
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
                "status": "OK",
                "response": response.json()
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
# Appels parallèles
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


    futures = []


    for index, row in sample.iterrows():

        futures.append(
            executor.submit(
                call_api,
                row
            )
        )


    for future in as_completed(futures):

        result = future.result()


        if result["status"] == "OK":

            success += 1

        else:

            errors += 1

            print(
                result
            )



duration = time.time() - start



# ==========================
# Résultats
# ==========================

print("===================")

print(
    "Simulation terminée"
)

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
    round(duration,2),
    "secondes"
)

print(
    "Débit :",
    round(N_ROWS / duration,2),
    "requêtes/sec"
)

print("===================")
