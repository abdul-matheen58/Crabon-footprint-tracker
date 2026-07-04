"""
Analytics Router — Endpoints for dashboard data visualization.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.user import User
from schemas.analytics import AnalyticsSummary
from utils.auth import get_current_user
from services.analytics import generate_dashboard_summary

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/summary", response_model=AnalyticsSummary)
async def get_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get the full analytics summary intended for the main dashboard."""
    summary = await generate_dashboard_summary(current_user.id, db)
    return summary
