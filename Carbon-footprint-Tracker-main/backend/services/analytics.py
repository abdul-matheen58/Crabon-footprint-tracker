"""
Analytics Service — Computes statistics, trends, and aggregations from user emissions.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, extract
from datetime import datetime, date, timedelta, timezone

from models.emission import EmissionLog
from schemas.analytics import AnalyticsSummary, CategoryBreakdown, DailyTrend


async def generate_dashboard_summary(user_id: str, db: AsyncSession) -> AnalyticsSummary:
    """Generate the full summary dataset needed for the dashboard."""
    
    today = date.today()
    first_day_this_month = today.replace(day=1)
    
    # Handle January correctly for last month calculation
    if today.month == 1:
        first_day_last_month = today.replace(year=today.year - 1, month=12, day=1)
    else:
        first_day_last_month = today.replace(month=today.month - 1, day=1)
        
    last_day_last_month = first_day_this_month - timedelta(days=1)
    thirty_days_ago = today - timedelta(days=30)
    
    # 1. Total All Time
    all_time_result = await db.execute(
        select(func.sum(EmissionLog.co2e_kg)).where(EmissionLog.user_id == user_id)
    )
    total_all_time = all_time_result.scalar() or 0.0

    # 2. Total This Month
    this_month_result = await db.execute(
        select(func.sum(EmissionLog.co2e_kg)).where(
            EmissionLog.user_id == user_id,
            EmissionLog.logged_at >= first_day_this_month
        )
    )
    total_this_month = this_month_result.scalar() or 0.0

    # 3. Total Last Month
    last_month_result = await db.execute(
        select(func.sum(EmissionLog.co2e_kg)).where(
            EmissionLog.user_id == user_id,
            EmissionLog.logged_at >= first_day_last_month,
            EmissionLog.logged_at <= last_day_last_month
        )
    )
    total_last_month = last_month_result.scalar() or 0.0
    
    # 4. Month Over Month Change (%)
    mom_change = 0.0
    if total_last_month > 0:
        mom_change = ((total_this_month - total_last_month) / total_last_month) * 100
        
    # 5. Category Breakdown (All Time or Last 30 Days)
    cat_result = await db.execute(
        select(EmissionLog.category, func.sum(EmissionLog.co2e_kg))
        .where(EmissionLog.user_id == user_id)
        .group_by(EmissionLog.category)
        .order_by(func.sum(EmissionLog.co2e_kg).desc())
    )
    cat_rows = cat_result.all()
    
    breakdown = []
    top_category = None
    if cat_rows:
        top_category = cat_rows[0][0]
        # total_all_time is already calculated
        for cat, val in cat_rows:
            pct = 0.0
            if total_all_time > 0:
                pct = (val / total_all_time) * 100
            breakdown.append(CategoryBreakdown(category=cat, co2e_kg=round(val, 2), percentage=round(pct, 1)))

    # 6. Daily Trends (Last 30 Days)
    trend_result = await db.execute(
        select(EmissionLog.logged_at, func.sum(EmissionLog.co2e_kg))
        .where(
            EmissionLog.user_id == user_id,
            EmissionLog.logged_at >= thirty_days_ago
        )
        .group_by(EmissionLog.logged_at)
        .order_by(EmissionLog.logged_at.asc())
    )
    trend_rows = trend_result.all()
    
    # Fill missing days with 0
    daily_trends = []
    trend_map = {row[0]: row[1] for row in trend_rows}
    
    for i in range(31):
        d = thirty_days_ago + timedelta(days=i)
        val = trend_map.get(d, 0.0)
        daily_trends.append(DailyTrend(date=d, co2e_kg=round(val, 2)))

    return AnalyticsSummary(
        total_co2e_all_time=round(total_all_time, 2),
        total_co2e_this_month=round(total_this_month, 2),
        total_co2e_last_month=round(total_last_month, 2),
        month_over_month_change_pct=round(mom_change, 1),
        top_category=top_category,
        category_breakdown=breakdown,
        daily_trends_30_days=daily_trends
    )
