"""
Goals Router — CRUD endpoints for user emission reduction goals.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from database import get_db
from models.user import User
from models.goal import Goal
from schemas.goal import GoalCreate, GoalUpdate, GoalResponse
from utils.auth import get_current_user

router = APIRouter(prefix="/goals", tags=["Goals"])


@router.post("/", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
async def create_goal(
    goal: GoalCreate, 
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new carbon reduction goal."""
    
    db_goal = Goal(
        user_id=current_user.id,
        title=goal.title,
        description=goal.description,
        target_co2e_kg=goal.target_co2e_kg,
        period=goal.period,
        target_date=goal.target_date
    )
    
    db.add(db_goal)
    await db.commit()
    await db.refresh(db_goal)
    
    return db_goal


@router.get("/", response_model=List[GoalResponse])
async def read_goals(
    status_filter: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all goals for the current user."""
    
    query = select(Goal).where(Goal.user_id == current_user.id)
    if status_filter:
        query = query.where(Goal.status == status_filter)
        
    result = await db.execute(query.order_by(Goal.target_date.asc()))
    
    return result.scalars().all()


@router.patch("/{goal_id}", response_model=GoalResponse)
async def update_goal(
    goal_id: str,
    goal_update: GoalUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a specific goal (e.g., mark as achieved)."""
    
    result = await db.execute(
        select(Goal).where(Goal.id == goal_id, Goal.user_id == current_user.id)
    )
    db_goal = result.scalars().first()
    
    if db_goal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
        
    update_data = goal_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_goal, key, value)
        
    await db.commit()
    await db.refresh(db_goal)
    
    return db_goal
