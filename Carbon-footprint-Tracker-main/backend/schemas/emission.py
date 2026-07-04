"""
Emission Schemas — Pydantic models for logging carbon emissions.
"""

from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class EmissionBase(BaseModel):
    category: str = Field(..., description="energy, transport, food, shopping, waste")
    sub_category: str = Field(...)
    activity_value: float = Field(..., gt=0, description="The amount of activity (e.g., 50.5)")
    unit: str = Field(...)
    notes: Optional[str] = None
    logged_at: date = Field(default_factory=date.today)


class EmissionCreate(EmissionBase):
    pass


class EmissionUpdate(BaseModel):
    category: Optional[str] = None
    sub_category: Optional[str] = None
    activity_value: Optional[float] = Field(None, gt=0)
    unit: Optional[str] = None
    notes: Optional[str] = None
    logged_at: Optional[date] = None


class EmissionResponse(EmissionBase):
    id: str
    co2e_kg: float
    user_id: str

    class Config:
        from_attributes = True
