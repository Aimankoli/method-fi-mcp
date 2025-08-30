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
    """
    Call Method API endpoint with simple error handling
    Returns either the response data or an error dict
    """
    url = f"{base_url}{endpoint}"
    
    headers = {
        "Method-Version": "2024-04-04",
        "Authorization": f"Bearer {method_api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=data if data else None,
            timeout=30
        )
        
        # Check if response is successful
        if response.status_code >= 200 and response.status_code < 300:
            try:
                return response.json()
            except json.JSONDecodeError:
                return {"success": True, "status_code": response.status_code}
        else:
            # Return error as dict instead of raising exception
            try:
                error_data = response.json()
                return {
                    "error": True,
                    "message": error_data.get('message', f'HTTP {response.status_code} error'),
                    "status_code": response.status_code,
                    "error_type": error_data.get('type', 'unknown_error'),
                    "error_code": error_data.get('code')
                }
            except json.JSONDecodeError:
                return {
                    "error": True,
                    "message": f"HTTP {response.status_code}: {response.text}",
                    "status_code": response.status_code
                }
                
    except requests.exceptions.Timeout:
        return {"error": True, "message": "Request timeout - Method API did not respond in time"}
    except requests.exceptions.ConnectionError:
        return {"error": True, "message": "Connection error - Unable to connect to Method API"}
    except requests.exceptions.RequestException as e:
        return {"error": True, "message": f"Request error: {str(e)}"}
    except Exception as e:
        return {"error": True, "message": f"Unexpected error: {str(e)}"}

async def main():
    # Test endpoint
    response = call_endpoint("/entities", "GET")
    print("Response:", response)

if __name__ == "__main__":
    asyncio.run(main())