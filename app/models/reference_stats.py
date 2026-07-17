from sqlalchemy import (
    Column,
    Integer,
    Float,
    String
)

from app.database.base import Base


class ReferenceStats(Base):

    __tablename__ = "reference_stats"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    feature_name = Column(
        String(100),
        nullable=False,
        unique=True
    )

    mean_value = Column(
        Float,
        nullable=False
    )

    std_value = Column(
        Float,
        nullable=False
    )

    min_value = Column(
        Float,
        nullable=False
    )

    max_value = Column(
        Float,
        nullable=False
    )

    sample_size = Column(
        Integer,
        nullable=False
    )
