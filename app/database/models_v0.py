from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime,
    JSON
)

from datetime import datetime

from app.database.base import Base



# ==========================
# Predictions modèle
# ==========================

class Prediction(Base):

    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True)

    client_id = Column(Integer)

    prediction = Column(Integer)

    score = Column(Float)

    threshold = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )



# ==========================
# Données entrantes API
# ==========================

class InputData(Base):

    __tablename__ = "input_data"

    id = Column(Integer, primary_key=True)

    client_id = Column(Integer)

    features = Column(JSON)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )



# ==========================
# Logs API
# ==========================

class ApiLog(Base):

    __tablename__ = "api_logs"

    id = Column(Integer, primary_key=True)

    endpoint = Column(String(100))

    status_code = Column(Integer)

    response_time = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )



# ==========================
# Santé système
# ==========================

class SystemHealthLog(Base):

    __tablename__ = "system_health_logs"

    id = Column(Integer, primary_key=True)

    cpu_usage = Column(Float)

    memory_usage = Column(Float)

    response_time = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )



# ==========================
# Statistiques référence X_train
# ==========================

class ReferenceStats(Base):

    __tablename__ = "reference_stats"

    id = Column(Integer, primary_key=True)

    feature_name = Column(String(100))

    mean_value = Column(Float)

    std_value = Column(Float)

    min_value = Column(Float)

    max_value = Column(Float)



# ==========================
# Drift monitoring
# ==========================

class DriftMonitoring(Base):

    __tablename__ = "drift_monitoring"

    id = Column(Integer, primary_key=True)

    feature_name = Column(String(100))

    psi = Column(Float)

    ks = Column(Float)

    status = Column(String(20))

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
