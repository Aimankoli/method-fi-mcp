from fastmcp.server.dependencies import get_http_headers
import os
import requests
from dotenv import load_dotenv
load_dotenv()
import json
import asyncio

base_url = os.getenv("BASE_URL", "https://dev.methodfi.com")
method_api_key = os.getenv("METHOD_API_KEY")
def call_endpoint(endpoint: str, method: str = "GET", data: dict = None):
    # Use development base URL for testing
    
    url = f"{base_url}{endpoint}"
    
    headers = {
        "Method-Version": "2024-04-04",
        "Authorization": f"Bearer {method_api_key}",
        "Content-Type": "application/json"
    }
    
    response = requests.request(
        method=method,
        url=url,
        headers=headers,
        json=data if data else None
    )
    
    return response.json()

async def main():
    # Create an individual entity
    entity_data = {
        "type": "individual",
        "individual": {
            "first_name": "Kevin",
            "last_name": "Doyle",
            "phone": "+16505555555",
            "email": "kevin.doyle@gmail.com",
            "dob": "1997-03-18"
        },
        "address": {
            "line1": "3300 N Interstate 35",
            "line2": None,
            "city": "Austin",
            "state": "TX",
            "zip": "78705"
        }
    }
    
    response = call_endpoint("/entities", "POST", entity_data)
    print(response)

if __name__ == "__main__":
    asyncio.run(main())