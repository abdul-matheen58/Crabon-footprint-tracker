"""
Smart Assistant Engine — A rule-based AI for context-aware responses.
Does not require external APIs. Parses intents and uses real DB context.
"""

import re
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Tuple, List, Dict, Any

from schemas.assistant import AssistantResponse, ActionItem
from services.analytics import generate_dashboard_summary
from services.calculator import FACTORS_DB


class IntentParser:
    """Parses user text to determine intent and extract entities."""
    
    @staticmethod
    def parse(message: str) -> Tuple[str, Dict[str, Any]]:
        msg_lower = message.lower()
        
        # 1. Check for Status/Progress intent
        if any(w in msg_lower for w in ["how am i", "progress", "status", "doing", "dashboard", "summary"]):
            return "STATUS_CHECK", {}
            
        # 2. Check for Tips intent
        if any(w in msg_lower for w in ["tip", "advice", "help", "reduce", "lower", "improve"]):
            category = None
            if "energy" in msg_lower or "electricity" in msg_lower: category = "energy"
            elif "car" in msg_lower or "drive" in msg_lower or "transport" in msg_lower: category = "transport"
            elif "food" in msg_lower or "meat" in msg_lower: category = "food"
            return "GET_TIPS", {"category": category}
            
        # 3. Check for Emission Logging (Rule-based NLP)
        if any(w in msg_lower for w in ["drove", "drive", "flew", "flight", "ate", "bought", "used"]):
            
            # Simple regex to find numbers
            num_match = re.search(r'\d+', msg_lower)
            value = float(num_match.group()) if num_match else 0.0
            
            if value > 0:
                if "drove" in msg_lower or "drive" in msg_lower:
                    if "km" in msg_lower or "kilometers" in msg_lower: # basic distance check
                        return "LOG_SUGGESTION", {
                            "category": "transport",
                            "sub_category": "petrol_car",
                            "activity_value": value,
                            "unit": "km"
                        }
                if "flew" in msg_lower or "flight" in msg_lower:
                    return "LOG_SUGGESTION", {
                        "category": "transport",
                        "sub_category": "domestic_flight",
                        "activity_value": value,
                        "unit": "km"
                    }
                # Could add more extraction logic here
                
        # 4. Check for Goal Setting
        if any(w in msg_lower for w in ["goal", "target", "aim"]):
            return "SET_GOAL", {}

        return "UNKNOWN", {}


class ContextEngine:
    """Builds a response based on the detected intent and user data."""
    
    @staticmethod
    async def process_message(message: str, user_id: str, db: AsyncSession) -> AssistantResponse:
        intent, entities = IntentParser.parse(message)
        
        if intent == "STATUS_CHECK":
            summary = await generate_dashboard_summary(user_id, db)
            
            text = f"This month you've emitted **{summary.total_co2e_this_month} kg CO₂**."
            
            if summary.total_co2e_last_month > 0:
                if summary.month_over_month_change_pct < 0:
                    text += f" That's **{abs(summary.month_over_month_change_pct)}% less** than last month! Great job! 🎉"
                else:
                    text += f" That's **{summary.month_over_month_change_pct}% more** than last month. 📈"
            
            if summary.top_category:
                top_pct = next((c.percentage for c in summary.category_breakdown if c.category == summary.top_category), 0)
                text += f"\n\nYour biggest emission source right now is **{summary.top_category}** ({top_pct}%). Focus on this category for the biggest impact."
                
            return AssistantResponse(
                text=text,
                intent_detected=intent,
                actions=[
                    ActionItem(type="view_analytics", label="View Full Analytics"),
                    ActionItem(type="view_tips", label=f"Tips to reduce {summary.top_category} emissions")
                ]
            )
            
        elif intent == "GET_TIPS":
            cat = entities.get("category")
            if cat:
                text = f"I'd love to help you reduce your **{cat}** emissions. Here's what you can do:"
            else:
                text = "Looking for ways to reduce your carbon footprint? I recommend checking out our personalized tips section:"
                
            return AssistantResponse(
                text=text,
                intent_detected=intent,
                actions=[
                    ActionItem(type="view_tips", label="Open Tips Library")
                ]
            )
            
        elif intent == "LOG_SUGGESTION":
            cat = entities.get("category")
            sub_cat = entities.get("sub_category")
            val = entities.get("activity_value")
            unit = entities.get("unit")
            
            # Look up label from factors DB
            label = "Activity"
            if cat in FACTORS_DB and sub_cat in FACTORS_DB[cat]:
                label = FACTORS_DB[cat][sub_cat].get("label", sub_cat)
            
            text = f"It looks like you want to log **{val} {unit}** for **{label}**. Should I log this for you?"
            
            return AssistantResponse(
                text=text,
                intent_detected=intent,
                actions=[
                    ActionItem(
                        type="log_emission", 
                        label="Yes, log it", 
                        payload={"category": cat, "sub_category": sub_cat, "activity_value": val, "unit": unit}
                    )
                ]
            )
            
        elif intent == "SET_GOAL":
            text = "Setting a goal is a fantastic way to stay motivated! Do you want to try reducing your monthly emissions by 10%?"
            return AssistantResponse(
                text=text,
                intent_detected=intent,
                actions=[
                    ActionItem(type="create_goal", label="Set a Goal")
                ]
            )
            
        else: # UNKNOWN
            text = "I'm your smart Carbon Assistant. I can help you check your progress, log emissions, or give you personalized tips to reduce your footprint. Just ask me things like 'How am I doing this month?' or 'I drove 40km today'."
            return AssistantResponse(
                text=text,
                intent_detected=intent,
                actions=[
                    ActionItem(type="view_analytics", label="Check Progress"),
                    ActionItem(type="view_tips", label="View Tips")
                ]
            )
