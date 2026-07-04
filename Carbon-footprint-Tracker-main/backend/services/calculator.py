"""
Calculation Service — Logic for computing CO2e based on emission factors.
"""

import json
import os
from fastapi import HTTPException, status

# Load factors on startup
FACTORS_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "emission_factors.json")

def load_factors():
    try:
        with open(FACTORS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading emission factors: {e}")
        return {}

FACTORS_DB = load_factors()


def calculate_co2e(category: str, sub_category: str, activity_value: float) -> float:
    """
    Calculate kg CO2e for a given activity.
    Throws HTTP 400 if category/sub-category not found.
    """
    cat_data = FACTORS_DB.get(category)
    if not cat_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Invalid category: {category}"
        )
        
    factor_data = cat_data.get(sub_category)
    if not factor_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Invalid sub-category: {sub_category} for category {category}"
        )
        
    factor = factor_data.get("factor", 0.0)
    
    # Calculate and round to 4 decimal places
    co2e_kg = round(activity_value * factor, 4)
    return co2e_kg
