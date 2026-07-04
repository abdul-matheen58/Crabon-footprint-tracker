"""
Tip Schemas — Pydantic models for carbon reduction tips.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TipResponse(BaseModel):
    id: int
    category: str
    title: str
    description: str
    impact_kg_month: float
    difficulty: str
    icon: Optional[str] = None
    
    class Config:
        from_attributes = True


class UserTipResponse(BaseModel):
    id: str
    tip_id: int
    status: str
    applied_at: Optional[datetime] = None
    tip: TipResponse

    class Config:
        from_attributes = True
