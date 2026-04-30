from fastapi import FastAPI, HTTPException
from models import TravelRecommendation
from mock_data import MEMBERS, PARTNER_CONFIGS, INVENTORY

app = FastAPI(title="Arrivia Agentic Recommendations API")

# --- MOCKED INTERNAL SERVICES ---

def get_member_data(member_id: str):
    if member_id not in MEMBERS:
        raise HTTPException(status_code=404, detail="Member not found")
    return MEMBERS[member_id]

def get_partner_config(partner_id: str):
    if partner_id not in PARTNER_CONFIGS:
        raise HTTPException(status_code=404, detail="Partner config not found")
    return PARTNER_CONFIGS[partner_id]

# --- THE POLICY ENGINE (Where the magic happens) ---

def apply_partner_rules(inventory: list, config: dict) -> list:
    """Filters global inventory based on strict partner rules."""
    filtered = []
    
    # Rule 1: Category Exclusions
    exclusions = config.get("exclude_categories", [])
    for item in inventory:
        if item["category"] not in exclusions:
            filtered.append(item)
            
    # Rule 2: Recommendation Caps
    cap = config.get("recommendation_cap")
    if cap is not None:
        filtered = filtered[:cap]
        
    return filtered

# --- THE AGENTIC ENDPOINT ---

@app.get("/api/v1/recommendations/{member_id}", response_model=list[TravelRecommendation])
async def get_agentic_recommendations(member_id: str):
    """
    MCP Tool Endpoint: AI Agents call this to get filtered travel options.
    """
    # 1. Fetch data safely
    member = get_member_data(member_id)
    partner_config = get_partner_config(member["partner_id"])
    
    # 2. Apply rules cleanly
    valid_recommendations = apply_partner_rules(INVENTORY, partner_config)
    
    return valid_recommendations