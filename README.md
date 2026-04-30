# Arrivia Agentic Recommendations API

This repository contains a proof of concept for the Agentic Travel Recommendations API. It allows AI agents to query travel inventories while enforcing partner business rules.

## Section A: Architecture and Trade-offs

### Architecture Overview
This system uses Python and FastAPI with Pydantic for data validation. It has three main layers. The first layer is mocked data that simulates external services. The second layer is a policy engine that filters travel options based on partner rules. The third layer is the API and MCP server. The MCP server allows AI agents to securely connect to the recommendation tool.

### Design Trade-offs
1. In-Memory Filtering vs. Database Queries. The policy engine currently filters data in memory. This works well for a prototype but is inefficient for large datasets. A production version would use database queries to filter data at the source.
2. Exposing REST and MCP APIs. I built both a standard REST endpoint and an MCP server. This duplicates some routing logic but keeps the system flexible. Standard frontends can use the REST API while AI agents connect through the MCP server.

### Handling Partner Configuration Changes
The system fetches the partner configuration on every request. If a partner adds a new rule, the next query will apply it automatically. In a real production environment, I would add a caching layer like Redis to improve performance while keeping the rules accurate.

## Section B: Production Readiness and Incident Response

### Incident Runbook Entry
**Alert:** A member reports the AI Concierge shows cruise recommendations even though their partner excludes cruises.

**Resolution Steps:**
1. Check the MCP server logs. Determine if the tool sent cruise options to the AI or if the AI generated them incorrectly.
2. Query the Partner Configuration Service directly. Confirm the exclusion rule is still active in the upstream database.
3. Review the travel inventory data. Verify the cruise items have the correct category tags.
4. Fix the issue based on the findings. Escalate to the configuration team if the rule is missing. Fix the database tags if the items are labeled incorrectly. Update the AI system prompt if it ignored the correct data.

### Required Reasoning Question
An AI coding assistant might suggest hardcoding the partner rules directly into the API using simple if statements. This is incorrect for a multi-tenant system. It forces the team to update the code and deploy the service every time a partner changes a rule.

I would catch this error by checking for separation of concerns. Business logic must be data-driven. I would verify the solution uses a flexible policy engine that reads rules from a database instead of using hardcoded tenant IDs.

## Section C: AI Usage Log

1. **Task:** Structuring the file system.
   * **Prompt:** How should I structure the files to separate the AI agent logic from the REST API in FastAPI?
   * **Result:** The AI suggested putting the MCP server and API routes in the same file.
   * **Decision:** I rejected this. I separated the files to keep the business logic easier to test.

2. **Task:** Writing unit tests.
   * **Prompt:** Generate Pytest edge cases for filtering a list of dictionaries based on maximum caps and category exclusions.
   * **Result:** The AI provided four useful test structures.
   * **Decision:** I kept the structure but rewrote the test data to match the specific travel variables used in this project.

3. **Task:** Creating the CLI script.
   * **Prompt:** Write a Python CLI script using the requests library to simulate a user asking for travel recommendations.
   * **Result:** The AI wrote a working loop but left out network error handling.
   * **Decision:** I kept the loop and added error handling so the script does not crash if the backend is offline.