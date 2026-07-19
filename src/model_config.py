# Ci-dessous avant optimisation par mise en cache du seuil de décision
#import json
#from pathlib import Path
#
#
#THRESHOLD_PATH = Path(
#    "artifacts/model/threshold.json"
#)
#
#
#def load_threshold():
#
#    with open(
#        THRESHOLD_PATH,
#        "r"
#    ) as f:
#        data = json.load(f)
#
#    return data["threshold"]

# ci-desssous version avec optimisation par mise en cache du seuil de décision
import json
from pathlib import Path
from functools import lru_cache


THRESHOLD_PATH = Path(
    "artifacts/model/threshold.json"
)


@lru_cache(maxsize=1)
def load_threshold():

    with open(
        THRESHOLD_PATH,
        "r"
    ) as f:
        data = json.load(f)

    return data["threshold"]
