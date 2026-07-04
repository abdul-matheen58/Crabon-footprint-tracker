"""
Carbon Footprint Platform — Main entry point for the FastAPI application.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

from config import settings
from database import init_db
from models.tip import Tip
from database import async_session
from sqlalchemy.future import select

# Routers
from routers.auth import router as auth_router
from routers.emissions import router as emissions_router
from routers.analytics import router as analytics_router
from routers.goals import router as goals_router
from routers.tips import router as tips_router
from routers.assistant import router as assistant_router





# Load reference data
async def seed_tips():
    async with async_session() as session:
        result = await session.execute(select(Tip).limit(1))
        if result.scalars().first():
            return # Already seeded
            
        # Add some initial tips
        tips_data = [
            Tip(category="transport", title="Use public transit", description="Taking the bus instead of driving can significantly reduce your footprint.", impact_kg_month=45.0, difficulty="medium", icon="bus"),
            Tip(category="energy", title="Switch to LED bulbs", description="LEDs use up to 90% less energy and last up to 25 times longer than traditional incandescent bulbs.", impact_kg_month=10.5, difficulty="easy", icon="lightbulb"),
            Tip(category="food", title="Have a meatless day", description="Skipping meat just one day a week can reduce your annual footprint substantially.", impact_kg_month=15.0, difficulty="easy", icon="leaf")
        ]
        session.add_all(tips_data)
        await session.commit()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    await seed_tips()
    yield
    # Shutdown
    # (Clean up if needed)


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "online"
    }

# Include routers
app.include_router(auth_router)
app.include_router(emissions_router)
app.include_router(analytics_router)
app.include_router(goals_router)
app.include_router(tips_router)
app.include_router(assistant_router)





