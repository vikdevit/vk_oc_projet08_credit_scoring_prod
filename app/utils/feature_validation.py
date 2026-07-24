import json
from pathlib import Path

LIMITS_PATH = Path(__file__).parent.parent / "feature_limits.json"

with open(LIMITS_PATH) as f:
    FEATURE_LIMITS = json.load(f)

