import json
import pandas as pd

reference_df = pd.read_parquet("./data/X_train_ml.parquet")

feature_limits = {}

for col in reference_df.columns:

    # Exclusion des identifiants techniques
    if col in [
        "SK_ID_CURR"
    ]:
        continue


    if pd.api.types.is_numeric_dtype(reference_df[col]):

        feature_limits[col] = {
            "min": float(reference_df[col].min()),
            "max": float(reference_df[col].max())
        }

with open("./app/feature_limits.json", "w") as f:
    json.dump(feature_limits, f, indent=4)

print("feature_limits.json créé")

print(len(feature_limits))

print("AMT_CREDIT_LOG" in feature_limits)
print(feature_limits["AMT_CREDIT_LOG"])
