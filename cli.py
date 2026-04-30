import requests
import sys

def main():
    print("Welcome to the Arrivia AI Concierge System")
    print("-" * 45)
    print("Available Test Users:")
    print(" - user_123 (Partner A: Max 3 items, no exclusions)")
    print(" - user_456 (Partner B: Excludes cruises)")
    print("-" * 45)

    while True:
        try:
            member_id = input("\nEnter Member ID (or 'quit' to exit): ").strip()
            
            if member_id.lower() == 'quit':
                print("Shutting down CLI...")
                break
            if not member_id:
                continue

            # Call our FastAPI backend
            url = f"http://127.0.0.1:8000/api/v1/recommendations/{member_id}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                print(f"\n✅ SUCCESS: Found {len(data)} valid recommendations for {member_id}:")
                for item in data:
                    print(f"   🏖️  {item['destination']} | {item['category'].capitalize()} | ${item['price']}")
            else:
                # Handle API errors gracefully
                error_msg = response.json().get('detail', 'Unknown error')
                print(f"\n❌ ERROR: {error_msg}")
                
        except requests.exceptions.ConnectionError:
            print("\n🚨 CRITICAL ERROR: Could not connect to the backend.")
            print("Make sure your FastAPI server is running with: uvicorn main:app --reload")
            sys.exit(1)
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()