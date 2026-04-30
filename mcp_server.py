from mcp.server.fastmcp import FastMCP
from main import get_member_data, get_partner_config, apply_partner_rules
from mock_data import INVENTORY

# Initialize the MCP Server
mcp = FastMCP("Arrivia-AI-Concierge")

@mcp.tool()
def get_travel_recommendations(member_id: str) -> str:
    """
    Fetches personalized travel recommendations for a loyalty member.
    This tool automatically enforces partner-specific business rules, 
    such as recommendation caps and category exclusions.
    """
    try:
        # 1. Fetch the data
        member = get_member_data(member_id)
        partner_config = get_partner_config(member["partner_id"])
        
        # 2. Apply the multi-tenant policy engine
        valid_recommendations = apply_partner_rules(INVENTORY, partner_config)
        
        # 3. Format the response cleanly for the LLM
        if not valid_recommendations:
            return "No valid travel recommendations found for this member's partner rules."
            
        result = f"Found {len(valid_recommendations)} recommendations:\n"
        for item in valid_recommendations:
            result += f"- {item['destination']} ({item['category']}): ${item['price']}\n"
            
        return result
        
    except Exception as e:
        # Graceful degradation for the AI agent
        return f"Error retrieving recommendations: {str(e)}"

if __name__ == "__main__":
    # This command allows the MCP server to run via standard input/output
    print("Starting Arrivia MCP Server...")
    mcp.run()