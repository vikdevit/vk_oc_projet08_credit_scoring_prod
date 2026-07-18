import pandas as pd
import requests
import time


# ==========================
# Configuration
# ==========================

API_URL = "https://vk-oc-projet08-credit-scoring-prod.onrender.com/predict"

DATA_PATH = "data/X_test_ml.parquet"

N_ROWS = 2


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
# Appels API
# ==========================

success = 0
errors = 0


for index, row in sample.iterrows():

    payload = {
        "features": row.to_dict()
    }


    try:

        response = requests.post(
            API_URL,
            json=payload,
            timeout=30
        )


        if response.status_code == 200:

            success += 1

            print(
                f"{index} OK",
                response.json()
            )

        else:

            errors += 1

            print(
                f"{index} ERROR",
                response.status_code
            )


    except Exception as e:

        errors += 1

        print(
            f"{index} Exception",
            e
        )


    # éviter de saturer Render
    time.sleep(0.2)



print("===================")
print("Simulation terminée")
print("Succès :", success)
print("Erreurs :", errors)
print("===================")
