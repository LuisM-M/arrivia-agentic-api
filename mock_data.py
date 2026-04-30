# Simulating the Member Data Service
MEMBERS = {
    "user_123": {
        "member_id": "user_123",
        "loyalty_tier": "Gold",
        "partner_id": "partner_A",
        "travel_history": [{"destination": "Hawaii", "type": "flight"}]
    },
    "user_456": {
        "member_id": "user_456",
        "loyalty_tier": "Silver",
        "partner_id": "partner_B", # Partner B hates cruises
        "travel_history": []
    }
}

# Simulating the Partner Configuration Service
PARTNER_CONFIGS = {
    "partner_A": {
        "partner_id": "partner_A",
        "recommendation_cap": 3,
        "exclude_categories": []
    },
    "partner_B": {
        "partner_id": "partner_B",
        "recommendation_cap": 5,
        "exclude_categories": ["cruise"] # The 2am incident scenario!
    }
}

# Simulating the global travel inventory (30,000+ itineraries simplified)
INVENTORY = [
    {"id": "t1", "destination": "Miami", "category": "hotel", "price": 200},
    {"id": "t2", "destination": "Bahamas", "category": "cruise", "price": 800},
    {"id": "t3", "destination": "New York", "category": "flight", "price": 300},
    {"id": "t4", "destination": "Alaska", "category": "cruise", "price": 1200},
]