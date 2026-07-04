"""
Assistant Router — Endpoint for chatting with the smart carbon assistant.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.user import User
from schemas.assistant import AssistantRequest, AssistantResponse
from utils.auth import get_current_user
from services.assistant import ContextEngine

router = APIRouter(prefix="/assistant", tags=["Assistant"])


@router.post("/chat", response_model=AssistantResponse)
async def chat_with_assistant(
    request: AssistantRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Send a message to the AI assistant to get context-aware responses and actions."""
    
    response = await ContextEngine.process_message(request.message, current_user.id, db)
    return response
