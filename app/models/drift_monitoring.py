from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime
)

from datetime import datetime

from app.database.base import Base


class DriftMonitoring(Base):

    __tablename__ = "drift_monitoring"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    feature_name = Column(
        String(100),
        nullable=False
    )

    psi = Column(
        Float,
        nullable=False
    )

    ks = Column(
        Float,
        nullable=False
    )

    threshold = Column(
        Float,
        nullable=False
    )

    status = Column(
        String(20),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
