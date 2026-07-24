import json

from app.utils.feature_validation import FEATURE_LIMITS


with open(
    "data/sample_request_client_ok.json"
) as f:
    payload = json.load(f)


errors = []


for feature, value in payload.items():

    if feature not in FEATURE_LIMITS:
        continue

    if not isinstance(value, (int, float)):
        continue

    limits = FEATURE_LIMITS[feature]

    if value < limits["min"]:
        errors.append(
            (
                feature,
                value,
                "inferieur",
                limits["min"]
            )
        )

    if value > limits["max"]:
        errors.append(
            (
                feature,
                value,
                "superieur",
                limits["max"]
            )
        )


print("Nombre erreurs :", len(errors))


for e in errors:
    print(e)
