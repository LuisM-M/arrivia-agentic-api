from pydantic import BaseModel
from typing import List, Optional

class Member(BaseModel):
    member_id: str
    loyalty_tier: str  # Silver, Gold, Platinum
    partner_id: str
    travel_history: List[dict]

class PartnerConfig(BaseModel):
    partner_id: str
    recommendation_cap: Optional[int] = None
    exclude_categories: List[str] = []

class TravelRecommendation(BaseModel):
    id: str
    destination: str
    category: str  # e.g., "flight", "hotel", "cruise"
    price: float