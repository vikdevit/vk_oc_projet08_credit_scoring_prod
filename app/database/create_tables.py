from app.database.connection import engine
from app.database.base import Base

# Import obligatoire de tous les modèles
from app.models.prediction import Prediction
from app.models.input_data import InputData
from app.models.api_log import ApiLog
from app.models.system_health_log import SystemHealthLog
from app.models.reference_stats import ReferenceStats
from app.models.drift_monitoring import DriftMonitoring


print("Création des tables...")

Base.metadata.drop_all(
    bind=engine
)

Base.metadata.create_all(
    bind=engine
)

print("Tables créées")
