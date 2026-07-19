# ci-dessous avant optimisation 
#import joblib
#from pathlib import Path
#
#
#MODEL_PATH = Path(
#    "artifacts/model/model.joblib"
#)
#
#
#def load_model():
#
#    return joblib.load(
#        MODEL_PATH
#    )

# ci-dessous après optimisation

import joblib
from pathlib import Path


MODEL_PATH = Path(
    "artifacts/model/model.joblib"
)


# Chargement unique du modèle au démarrage du module
MODEL = joblib.load(
    MODEL_PATH
)


def load_model():

   return MODEL
