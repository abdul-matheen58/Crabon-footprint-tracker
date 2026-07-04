"""
Goal Schemas — Pydantic models for user goals.
"""

from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class GoalBase(BaseModel):
    title: str = Field(..., description="Goal title, e.g., 'Reduce car usage'")
    description: Optional[str] = None
    target_co2e_kg: float = Field(..., gt=0)
    period: str = Field(..., description="weekly, monthly, yearly")
    target_date: date


class GoalCreate(GoalBase):
    pass


class GoalUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    target_co2e_kg: Optional[float] = Field(None, gt=0)
    period: Optional[str] = None
    status: Optional[str] = Field(None, description="active, achieved, failed, cancelled")
    target_date: Optional[date] = None


class GoalResponse(GoalBase):
    id: str
    user_id: str
    status: str
    start_date: date

    class Config:
        from_attributes = True
