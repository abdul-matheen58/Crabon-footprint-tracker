"""
Emissions Router — CRUD endpoints for taking user activity and logging emissions.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
from typing import List

from database import get_db
from models.user import User
from models.emission import EmissionLog
from schemas.emission import EmissionCreate, EmissionUpdate, EmissionResponse
from utils.auth import get_current_user
from services.calculator import calculate_co2e

router = APIRouter(prefix="/emissions", tags=["Emissions"])


@router.post("/", response_model=EmissionResponse, status_code=status.HTTP_201_CREATED)
async def create_emission(
    emission: EmissionCreate, 
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Log a new carbon emission activity."""
    
    # Calculate footprint based on activity value
    co2e_value = calculate_co2e(
        emission.category, 
        emission.sub_category, 
        emission.activity_value
    )
    
    db_emission = EmissionLog(
        user_id=current_user.id,
        category=emission.category,
        sub_category=emission.sub_category,
        activity_value=emission.activity_value,
        unit=emission.unit,
        co2e_kg=co2e_value,
        notes=emission.notes,
        logged_at=emission.logged_at
    )
    
    db.add(db_emission)
    await db.commit()
    await db.refresh(db_emission)
    
    return db_emission


@router.get("/", response_model=List[EmissionResponse])
async def read_emissions(
    skip: int = 0, 
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all emission logs for the current user."""
    
    result = await db.execute(
        select(EmissionLog)
        .where(EmissionLog.user_id == current_user.id)
        .order_by(desc(EmissionLog.logged_at), desc(EmissionLog.created_at))
        .offset(skip)
        .limit(limit)
    )
    
    return result.scalars().all()


@router.get("/{emission_id}", response_model=EmissionResponse)
async def read_emission(
    emission_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific emission log."""
    
    result = await db.execute(
        select(EmissionLog)
        .where(EmissionLog.id == emission_id, EmissionLog.user_id == current_user.id)
    )
    db_emission = result.scalars().first()
    
    if db_emission is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Emission log not found")
        
    return db_emission


@router.delete("/{emission_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_emission(
    emission_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a specific emission log."""
    
    result = await db.execute(
        select(EmissionLog)
        .where(EmissionLog.id == emission_id, EmissionLog.user_id == current_user.id)
    )
    db_emission = result.scalars().first()
    
    if db_emission is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Emission log not found")
        
    await db.delete(db_emission)
    await db.commit()
    
    return None
