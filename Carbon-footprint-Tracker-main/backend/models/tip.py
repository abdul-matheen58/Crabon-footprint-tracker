"""
Tip Model — Stores carbon reduction recommendations.
UserTip tracks which tips a user has applied.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Tip(Base):
    """
    Carbon reduction tip/recommendation.
    Seeded from a curated list on app startup.
    """

    __tablename__ = "tips"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(50), nullable=False)          # energy, transport, food, shopping, waste
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    impact_kg_month = Column(Float, nullable=False)        # est. monthly CO₂ savings in kg
    difficulty = Column(String(20), nullable=False)        # easy, medium, hard
    icon = Column(String(50), nullable=True)               # emoji or icon name
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    user_tips = relationship("UserTip", back_populates="tip", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Tip(id={self.id}, title={self.title}, impact={self.impact_kg_month}kg/mo)>"


class UserTip(Base):
    """Tracks which tips a user has bookmarked or applied."""

    __tablename__ = "user_tips"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    tip_id = Column(
        Integer,
        ForeignKey("tips.id", ondelete="CASCADE"),
        nullable=False,
    )
    status = Column(String(20), default="bookmarked")  # bookmarked, applied, dismissed
    applied_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    user = relationship("User", back_populates="user_tips")
    tip = relationship("Tip", back_populates="user_tips")

    def __repr__(self):
        return f"<UserTip(user_id={self.user_id}, tip_id={self.tip_id}, status={self.status})>"
