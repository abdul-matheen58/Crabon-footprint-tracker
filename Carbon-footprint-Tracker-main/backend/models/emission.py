"""
Emission Log Model — Stores individual carbon emission entries.
Each entry ties an activity to its calculated CO₂e value.
"""

import uuid
from datetime import datetime, date, timezone
from sqlalchemy import Column, String, Float, Date, DateTime, Text, ForeignKey, Index
from sqlalchemy.orm import relationship
from database import Base


class EmissionLog(Base):
    """
    Individual emission log entry.
    
    The CO₂e value is computed server-side using:
        co2e_kg = activity_value × emission_factor
    
    Categories: energy, transport, food, shopping, waste
    """

    __tablename__ = "emission_logs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    category = Column(String(50), nullable=False)       # energy, transport, food, shopping, waste
    sub_category = Column(String(100), nullable=False)   # electricity, petrol_car, beef, etc.
    activity_value = Column(Float, nullable=False)       # numerical value (e.g., 50 km, 200 kWh)
    unit = Column(String(30), nullable=False)            # km, kWh, kg, item, etc.
    co2e_kg = Column(Float, nullable=False)              # calculated CO₂ equivalent in kg
    notes = Column(Text, nullable=True)                  # optional user notes
    logged_at = Column(Date, nullable=False, default=date.today)  # date of the activity
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationship
    user = relationship("User", back_populates="emissions")

    # Composite index for efficient queries
    __table_args__ = (
        Index("idx_user_category_date", "user_id", "category", "logged_at"),
    )

    def __repr__(self):
        return (
            f"<EmissionLog(id={self.id}, category={self.category}, "
            f"sub_category={self.sub_category}, co2e_kg={self.co2e_kg})>"
        )
