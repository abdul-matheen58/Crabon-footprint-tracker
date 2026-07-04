import pytest
from httpx import AsyncClient
from main import app
from database import engine, Base

@pytest.fixture(autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Register
        reg_res = await ac.post("/auth/register", json={
            "email": "test@example.com",
            "name": "Test User",
            "password": "testpassword123"
        })
        assert reg_res.status_code == 201
        
        # Login
        login_res = await ac.post("/auth/login", data={
            "username": "test@example.com",
            "password": "testpassword123"
        })
        assert login_res.status_code == 200
        assert "access_token" in login_res.json()
