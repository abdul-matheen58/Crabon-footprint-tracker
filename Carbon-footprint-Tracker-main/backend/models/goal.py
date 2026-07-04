"""
Goal Model — Tracks user carbon reduction goals.
"""

import uuid
from datetime import datetime, date, timezone
from sqlalchemy import Column, String, Float, Date, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Goal(Base):
    """
    User-defined carbon reduction goal.
    
    status values: active, achieved, failed, cancelled
    period values: weekly, monthly, yearly
    """

    __tablename__ = "goals"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    target_co2e_kg = Column(Float, nullable=False)    # target max CO₂e for the period
    period = Column(String(20), nullable=False)        # weekly, monthly, yearly
    status = Column(String(20), default="active")      # active, achieved, failed, cancelled
    start_date = Column(Date, nullable=False, default=date.today)
    target_date = Column(Date, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationship
    user = relationship("User", back_populates="goals")

    def __repr__(self):
        return (
            f"<Goal(id={self.id}, title={self.title}, "
            f"target={self.target_co2e_kg}kg, status={self.status})>"
        )
