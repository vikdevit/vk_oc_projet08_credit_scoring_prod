"""
Profiling de la fonction de prédiction.

Objectif :
- mesurer où est consommé le temps d'exécution
- identifier les goulots d'étranglement
- préparer les optimisations (Projet OC 9.1)

Exécution :

PYTHONPATH=. uv run python scripts/profile_prediction.py
"""

import cProfile
import pstats

from app.predictor import predict
from app.database.session import SessionLocal


# ==========================
# Exemple de client
# ==========================

import pandas as pd

X = pd.read_parquet("data/X_test_ml.parquet")

features = X.iloc[0].to_dict()


# ==========================
# Session base
# ==========================

db = SessionLocal()


# ==========================
# Profiling
# ==========================

profiler = cProfile.Profile()

profiler.enable()

predict(
    features=features,
    db=db
)

profiler.disable()


# ==========================
# Affichage des fonctions
# les plus coûteuses
# ==========================

stats = pstats.Stats(profiler)

stats.sort_stats("cumulative")

stats.print_stats(30)


db.rollback()
db.close()
