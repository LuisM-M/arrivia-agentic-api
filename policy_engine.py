def apply_partner_rules(inventory: list, config: dict) -> list:
    """Filters global inventory based on strict partner rules."""
    
    filtered_inventory = []
    
    # Extract rules from the partner configuration
    # We use .get() so it defaults to an empty list or None if the rule does not exist
    exclusions = config.get("exclude_categories", [])
    max_items = config.get("recommendation_cap")
    
    # Step 1: Filter out the excluded categories (The 'WHERE' clause)
    for item in inventory:
        # If the item category is forbidden, we skip it entirely
        if item["category"] in exclusions:
            continue
            
        # If it passes the check, we add it to our new list
        filtered_inventory.append(item)
        
    # Step 2: Enforce the maximum item limit (The 'LIMIT' clause)
    if max_items is not None:
        # We slice the array to only keep the allowed number of items
        filtered_inventory = filtered_inventory[:max_items]
        
    return filtered_inventory