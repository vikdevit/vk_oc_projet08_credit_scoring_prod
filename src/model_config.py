import json
from pathlib import Path


THRESHOLD_PATH = Path(
    "artifacts/model/threshold.json"
)


def load_threshold():

    with open(
        THRESHOLD_PATH,
        "r"
    ) as f:
        data = json.load(f)

    return data["threshold"]
