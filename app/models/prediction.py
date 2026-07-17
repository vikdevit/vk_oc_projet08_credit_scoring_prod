from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime
)

from datetime import datetime

from app.database.base import Base


class Prediction(Base):

    __tablename__ = "predictions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    client_id = Column(
        Integer,
        nullable=False
    )

    prediction = Column(
        Integer,
        nullable=False
    )

    score = Column(
        Float,
        nullable=False
    )

    threshold = Column(
        Float,
        nullable=False
    )

    # Nouvelle colonne
    model_version = Column(
        String(50),
        nullable=False
    )

    # Nouvelle colonne
    latency_ms = Column(
        Float,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
