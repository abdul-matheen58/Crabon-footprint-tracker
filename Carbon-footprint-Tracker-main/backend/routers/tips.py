"""
Tips Router — Endpoints for viewing and managing carbon reduction tips.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List

from database import get_db
from models.user import User
from models.tip import Tip, UserTip
from schemas.tip import TipResponse, UserTipResponse
from utils.auth import get_current_user

router = APIRouter(prefix="/tips", tags=["Tips"])


@router.get("/", response_model=List[TipResponse])
async def get_all_tips(
    category: str = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all available carbon reduction tips, optionally filtered by category."""
    
    query = select(Tip)
    if category:
        query = query.where(Tip.category == category)
        
    result = await db.execute(query.order_by(Tip.impact_kg_month.desc()))
    return result.scalars().all()


@router.post("/{tip_id}/bookmark", response_model=UserTipResponse, status_code=status.HTTP_201_CREATED)
async def bookmark_tip(
    tip_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Bookmark or apply a specific tip for the user."""
    
    # Check if tip exists
    tip_result = await db.execute(select(Tip).where(Tip.id == tip_id))
    if not tip_result.scalars().first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tip not found")
        
    # Check if already bookmarked
    existing_result = await db.execute(
        select(UserTip).where(UserTip.tip_id == tip_id, UserTip.user_id == current_user.id)
    )
    existing_user_tip = existing_result.scalars().first()
    
    if existing_user_tip:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tip already bookmarked")
        
    new_user_tip = UserTip(
        user_id=current_user.id,
        tip_id=tip_id,
        status="bookmarked"
    )
    
    db.add(new_user_tip)
    await db.commit()
    
    # Reload with the relationship
    result = await db.execute(
        select(UserTip)
        .options(selectinload(UserTip.tip))
        .where(UserTip.id == new_user_tip.id)
    )
    
    return result.scalars().first()


@router.get("/my-tips", response_model=List[UserTipResponse])
async def get_my_tips(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all tips bookmarked or applied by the user."""
    
    result = await db.execute(
        select(UserTip)
        .options(selectinload(UserTip.tip))
        .where(UserTip.user_id == current_user.id)
    )
    
    return result.scalars().all()
