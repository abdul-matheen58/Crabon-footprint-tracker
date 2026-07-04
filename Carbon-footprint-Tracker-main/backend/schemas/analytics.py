"""
Analytics Schemas — Pydantic models for returning emission statistics.
"""

from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import date


class CategoryBreakdown(BaseModel):
    category: str
    co2e_kg: float
    percentage: float


class DailyTrend(BaseModel):
    date: date
    co2e_kg: float


class AnalyticsSummary(BaseModel):
    total_co2e_all_time: float
    total_co2e_this_month: float
    total_co2e_last_month: float
    month_over_month_change_pct: float
    top_category: Optional[str]
    category_breakdown: List[CategoryBreakdown]
    daily_trends_30_days: List[DailyTrend]
