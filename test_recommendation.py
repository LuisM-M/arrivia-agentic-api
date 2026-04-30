import pytest
from policy_engine import apply_partner_rules

# --- Test Data ---
MOCK_INVENTORY = [
    {"id": "t1", "destination": "Miami", "category": "hotel", "price": 200},
    {"id": "t2", "destination": "Bahamas", "category": "cruise", "price": 800},
    {"id": "t3", "destination": "New York", "category": "flight", "price": 300},
    {"id": "t4", "destination": "Alaska", "category": "cruise", "price": 1200},
    {"id": "t5", "destination": "Cancun", "category": "resort", "price": 500},
]

def test_no_rules_returns_all():
    """Test that an empty config returns the full inventory."""
    config = {"partner_id": "open_partner"}
    result = apply_partner_rules(MOCK_INVENTORY, config)
    assert len(result) == 5

def test_category_exclusion():
    """Test that category exclusions strictly remove matching items."""
    config = {"partner_id": "no_cruise_partner", "exclude_categories": ["cruise"]}
    result = apply_partner_rules(MOCK_INVENTORY, config)
    
    assert len(result) == 3
    # Ensure no cruises snuck in
    for item in result:
        assert item["category"] != "cruise"

def test_recommendation_cap():
    """Test that the engine respects the maximum recommendation cap."""
    config = {"partner_id": "capped_partner", "recommendation_cap": 2}
    result = apply_partner_rules(MOCK_INVENTORY, config)
    
    assert len(result) == 2

def test_combined_rules():
    """Test both exclusions and caps applied simultaneously."""
    config = {
        "partner_id": "strict_partner", 
        "exclude_categories": ["cruise"], 
        "recommendation_cap": 1
    }
    result = apply_partner_rules(MOCK_INVENTORY, config)
    
    assert len(result) == 1
    assert result[0]["category"] != "cruise"