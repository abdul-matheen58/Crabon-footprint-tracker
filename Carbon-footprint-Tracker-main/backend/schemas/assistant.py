"""
Assistant Schemas — Pydantic models for the smart assistant endpoint.
"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class AssistantRequest(BaseModel):
    message: str


class ActionItem(BaseModel):
    type: str # 'log_emission', 'view_tips', 'create_goal', 'view_analytics'
    label: str
    payload: Optional[Dict[str, Any]] = None


class AssistantResponse(BaseModel):
    text: str
    actions: List[ActionItem] = []
    intent_detected: str
