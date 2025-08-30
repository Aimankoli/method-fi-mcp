from fastmcp import FastMCP
from dotenv import load_dotenv
import os
import asyncio
from server.api import call_endpoint
from typing import List, Dict, Optional, Annotated
from pydantic import Field

load_dotenv()
print(f"Method API Key in server: {os.getenv('METHOD_API_KEY')}")

mcp = FastMCP()

@mcp.tool(name="HelloWorld", description="A simple hello world tool")
def hello_world():
    return f"Hello, World! my API key is {os.getenv('METHOD_API_KEY')}"

# ===== ENTITY ENDPOINTS =====

@mcp.tool(name="create_individual", description="Create an individual entity in Method")
async def create_individual(
    first_name: Annotated[str, Field(description="First name of the individual")],
    last_name: Annotated[str, Field(description="Last name of the individual")],
    phone: Annotated[str, Field(description="Phone number (e.g., +16505555555)")],
    email: Annotated[str, Field(description="Email address")],
    dob: Annotated[str, Field(description="Date of birth in yyyy-mm-dd format")],
    street_address: Annotated[str, Field(description="Street address line 1")],
    city: Annotated[str, Field(description="City")],
    state: Annotated[str, Field(description="State (2 letter code, e.g., TX)")],
    zip: Annotated[str, Field(description="ZIP code")],
    street_address_2: Annotated[Optional[str], Field(description="Street address line 2")] = None,
) -> Dict:
    """Create an individual entity with required fields"""
    entity_data = {
        "type": "individual",
        "individual": {
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "email": email,
            "dob": dob
        },
        "address": {
            "line1": street_address,
            "line2": street_address_2,
            "city": city,
            "state": state,
            "zip": zip
        }
    }
    return call_endpoint("/entities", "POST", data=entity_data)

@mcp.tool(name="create_corporation", description="Create a corporation entity in Method")
async def create_corporation(
    name: Annotated[str, Field(description="Corporation name")],
    street_address: Annotated[str, Field(description="Street address line 1")],
    city: Annotated[str, Field(description="City")],
    state: Annotated[str, Field(description="State (2 letter code)")],
    zip: Annotated[str, Field(description="ZIP code")],
    owner_first_name: Annotated[str, Field(description="Owner's first name")],
    owner_last_name: Annotated[str, Field(description="Owner's last name")],
    owner_phone: Annotated[str, Field(description="Owner's phone number")],
    owner_email: Annotated[str, Field(description="Owner's email")],
    owner_dob: Annotated[str, Field(description="Owner's date of birth (yyyy-mm-dd)")],
    owner_street_address: Annotated[str, Field(description="Owner's street address")],
    owner_city: Annotated[str, Field(description="Owner's city")],
    owner_state: Annotated[str, Field(description="Owner's state")],
    owner_zip: Annotated[str, Field(description="Owner's ZIP code")],
    dba: Annotated[Optional[str], Field(description="Doing business as name")] = None,
    ein: Annotated[Optional[str], Field(description="Employer Identification Number")] = None,
    street_address_2: Annotated[Optional[str], Field(description="Street address line 2")] = None,
) -> Dict:
    """Create a corporation entity"""
    entity_data = {
        "type": "corporation",
        "corporation": {
            "name": name,
            "dba": dba,
            "ein": ein,
            "owners": [
                {
                    "first_name": owner_first_name,
                    "last_name": owner_last_name,
                    "phone": owner_phone,
                    "email": owner_email,
                    "dob": owner_dob,
                    "address": {
                        "line1": owner_street_address,
                        "line2": None,
                        "city": owner_city,
                        "state": owner_state,
                        "zip": owner_zip
                    }
                }
            ]
        },
        "address": {
            "line1": street_address,
            "line2": street_address_2,
            "city": city,
            "state": state,
            "zip": zip
        }
    }
    return call_endpoint("/entities", "POST", data=entity_data)

@mcp.tool(name="list_entities", description="List all entities")
async def list_entities(
    entity_type: Annotated[Optional[str], Field(description="Filter by type: individual or corporation")] = None,
    status: Annotated[Optional[str], Field(description="Filter by status: active, incomplete, disabled")] = None,
    page_cursor: Annotated[Optional[str], Field(description="Cursor for pagination")] = None,
    page_limit: Annotated[Optional[int], Field(description="Number of entities per page (max 250)")] = None,
) -> Dict:
    """List all entities with optional filters"""
    params = {}
    if entity_type:
        params["type"] = entity_type
    if status:
        params["status"] = status
    if page_cursor:
        params["page[cursor]"] = page_cursor
    if page_limit:
        params["page[limit]"] = min(page_limit, 250)
    
    if params:
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        endpoint = f"/entities?{query_string}"
    else:
        endpoint = "/entities"
    
    return call_endpoint(endpoint, "GET")

@mcp.tool(name="retrieve_entity", description="Retrieve a specific entity by ID")
async def retrieve_entity(
    entity_id: Annotated[str, Field(description="The entity ID to retrieve (e.g., ent_au22b1fbFJbp8)")]
) -> Dict:
    """Retrieve entity details by ID"""
    return call_endpoint(f"/entities/{entity_id}", "GET")

@mcp.tool(name="update_entity", description="Update an entity")
async def update_entity(
    entity_id: Annotated[str, Field(description="The entity ID to update")],
    first_name: Annotated[Optional[str], Field(description="Updated first name")] = None,
    last_name: Annotated[Optional[str], Field(description="Updated last name")] = None,
    phone: Annotated[Optional[str], Field(description="Updated phone number")] = None,
    email: Annotated[Optional[str], Field(description="Updated email")] = None,
    dob: Annotated[Optional[str], Field(description="Updated date of birth (yyyy-mm-dd)")] = None,
) -> Dict:
    """Update entity information for individuals"""
    update_data = {}
    individual_updates = {}
    
    if first_name:
        individual_updates["first_name"] = first_name
    if last_name:
        individual_updates["last_name"] = last_name
    if phone:
        individual_updates["phone"] = phone
    if email:
        individual_updates["email"] = email
    if dob:
        individual_updates["dob"] = dob
    
    if individual_updates:
        update_data["individual"] = individual_updates
    
    return call_endpoint(f"/entities/{entity_id}", "PUT", data=update_data)

# ===== ENTITY CONNECT ENDPOINTS =====

@mcp.tool(name="create_entity_connect", description="Create a connect session to discover entity's liability accounts")
async def create_entity_connect(
    entity_id: Annotated[str, Field(description="The entity ID to connect")]
) -> Dict:
    """Create a connect session to discover entity's liability accounts"""
    return call_endpoint(f"/entities/{entity_id}/connect", "POST")

@mcp.tool(name="retrieve_entity_connect", description="Retrieve a specific connect session")
async def retrieve_entity_connect(
    entity_id: Annotated[str, Field(description="The entity ID")],
    connect_id: Annotated[str, Field(description="The connect session ID")]
) -> Dict:
    """Retrieve a specific connect session"""
    return call_endpoint(f"/entities/{entity_id}/connect/{connect_id}", "GET")

@mcp.tool(name="list_entity_connects", description="List connects for an entity")
async def list_entity_connects(
    entity_id: Annotated[str, Field(description="The entity ID")]
) -> Dict:
    """List all connects for a specific entity"""
    return call_endpoint(f"/entities/{entity_id}/connect", "GET")

# ===== CREDIT SCORE ENDPOINTS =====

@mcp.tool(name="create_credit_score", description="Get entity's credit score")
async def create_credit_score(
    entity_id: Annotated[str, Field(description="The entity ID")]
) -> Dict:
    """Create a credit score request for an entity"""
    return call_endpoint(f"/entities/{entity_id}/credit_scores", "POST")

@mcp.tool(name="retrieve_credit_score", description="Retrieve a specific credit score")
async def retrieve_credit_score(
    entity_id: Annotated[str, Field(description="The entity ID")],
    credit_score_id: Annotated[str, Field(description="The credit score ID")]
) -> Dict:
    """Retrieve a specific credit score"""
    return call_endpoint(f"/entities/{entity_id}/credit_scores/{credit_score_id}", "GET")

@mcp.tool(name="list_credit_scores", description="List credit scores for an entity")
async def list_credit_scores(
    entity_id: Annotated[str, Field(description="The entity ID")]
) -> Dict:
    """List all credit scores for a specific entity"""
    return call_endpoint(f"/entities/{entity_id}/credit_scores", "GET")

# ===== ACCOUNT ENDPOINTS =====

@mcp.tool(name="create_ach_account", description="Create an ACH account (checking or savings)")
async def create_ach_account(
    entity_id: Annotated[str, Field(description="The entity ID that owns this account")],
    routing_number: Annotated[str, Field(description="Bank routing number (9 digits)")],
    account_number: Annotated[str, Field(description="Bank account number")],
    account_type: Annotated[str, Field(description="Account type: checking or savings")]
) -> Dict:
    """Create an ACH account"""
    account_data = {
        "holder_id": entity_id,
        "ach": {
            "routing": routing_number,
            "number": account_number,
            "type": account_type
        }
    }
    return call_endpoint("/accounts", "POST", data=account_data)

@mcp.tool(name="create_liability_account", description="Create a liability account (credit card, loan, etc.)")
async def create_liability_account(
    entity_id: Annotated[str, Field(description="The entity ID that owns this account")],
    merchant_id: Annotated[str, Field(description="The merchant ID (e.g., mch_2)")],
    account_number: Annotated[str, Field(description="The account number")]
) -> Dict:
    """Create a liability account"""
    account_data = {
        "holder_id": entity_id,
        "liability": {
            "mch_id": merchant_id,
            "account_number": account_number
        }
    }
    return call_endpoint("/accounts", "POST", data=account_data)

@mcp.tool(name="list_accounts", description="List all accounts")
async def list_accounts(
    entity_id: Annotated[Optional[str], Field(description="Filter by entity ID")] = None,
    page_cursor: Annotated[Optional[str], Field(description="Cursor for pagination")] = None,
    page_limit: Annotated[Optional[int], Field(description="Number of accounts per page")] = None,
) -> Dict:
    """List all accounts with optional filters"""
    params = {}
    if entity_id:
        params["holder_id"] = entity_id
    if page_cursor:
        params["page[cursor]"] = page_cursor
    if page_limit:
        params["page[limit]"] = min(page_limit, 250)
    
    if params:
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        endpoint = f"/accounts?{query_string}"
    else:
        endpoint = "/accounts"
    
    return call_endpoint(endpoint, "GET")

@mcp.tool(name="retrieve_account", description="Retrieve a specific account by ID")
async def retrieve_account(
    account_id: Annotated[str, Field(description="The account ID to retrieve")]
) -> Dict:
    """Retrieve account details by ID"""
    return call_endpoint(f"/accounts/{account_id}", "GET")

# ===== ACCOUNT UPDATES ENDPOINTS =====

@mcp.tool(name="create_account_update", description="Create an account update to get real-time data")
async def create_account_update(
    account_id: Annotated[str, Field(description="The account ID to update")]
) -> Dict:
    """Create an update for real-time account data"""
    return call_endpoint(f"/accounts/{account_id}/updates", "POST")

@mcp.tool(name="retrieve_account_update", description="Retrieve a specific account update")
async def retrieve_account_update(
    account_id: Annotated[str, Field(description="The account ID")],
    update_id: Annotated[str, Field(description="The update ID")]
) -> Dict:
    """Retrieve a specific account update"""
    return call_endpoint(f"/accounts/{account_id}/updates/{update_id}", "GET")

@mcp.tool(name="list_account_updates", description="List updates for an account")
async def list_account_updates(
    account_id: Annotated[str, Field(description="The account ID")],
    page_limit: Annotated[Optional[int], Field(description="Number of updates per page")] = None,
) -> Dict:
    """List all updates for a specific account"""
    params = {}
    if page_limit:
        params["page[limit]"] = min(page_limit, 250)
    
    query_string = "&".join([f"{k}={v}" for k, v in params.items()]) if params else ""
    endpoint = f"/accounts/{account_id}/updates?{query_string}" if query_string else f"/accounts/{account_id}/updates"
    return call_endpoint(endpoint, "GET")

# ===== BALANCE ENDPOINTS =====

@mcp.tool(name="create_balance", description="Get real-time balance for an account")
async def create_balance(
    account_id: Annotated[str, Field(description="The account ID")]
) -> Dict:
    """Create a balance request to get real-time balance"""
    return call_endpoint(f"/accounts/{account_id}/balances", "POST")

@mcp.tool(name="retrieve_balance", description="Retrieve a specific balance")
async def retrieve_balance(
    account_id: Annotated[str, Field(description="The account ID")],
    balance_id: Annotated[str, Field(description="The balance ID")]
) -> Dict:
    """Retrieve a specific balance"""
    return call_endpoint(f"/accounts/{account_id}/balances/{balance_id}", "GET")

@mcp.tool(name="list_balances", description="List balances for an account")
async def list_balances(
    account_id: Annotated[str, Field(description="The account ID")]
) -> Dict:
    """List all balances for an account"""
    return call_endpoint(f"/accounts/{account_id}/balances", "GET")

# ===== PAYMENT ENDPOINTS =====

@mcp.tool(name="create_payment", description="Create a payment between accounts")
async def create_payment(
    amount: Annotated[int, Field(description="Payment amount in cents (e.g., 5000 = $50.00)")],
    source: Annotated[str, Field(description="Source account ID (ACH account)")],
    destination: Annotated[str, Field(description="Destination account ID (liability account)")],
    description: Annotated[str, Field(description="Payment description (max 10 characters)")],
    dry_run: Annotated[Optional[bool], Field(description="Simulate payment without processing")] = False,
) -> Dict:
    """Create a payment from source to destination account"""
    # Validate description length
    if len(description) > 10:
        return {
            "error": True,
            "message": "Description must be 10 characters or less"
        }
    
    payment_data = {
        "amount": amount,
        "source": source,
        "destination": destination,
        "description": description
    }
    if dry_run:
        payment_data["dry_run"] = dry_run
    
    return call_endpoint("/payments", "POST", data=payment_data)

@mcp.tool(name="list_payments", description="List all payments")
async def list_payments(
    page_cursor: Annotated[Optional[str], Field(description="Cursor for pagination")] = None,
    page_limit: Annotated[Optional[int], Field(description="Number of payments per page")] = None,
) -> Dict:
    """List all payments"""
    params = {}
    if page_cursor:
        params["page[cursor]"] = page_cursor
    if page_limit:
        params["page[limit]"] = min(page_limit, 250)
    
    if params:
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        endpoint = f"/payments?{query_string}"
    else:
        endpoint = "/payments"
    
    return call_endpoint(endpoint, "GET")

@mcp.tool(name="retrieve_payment", description="Retrieve a specific payment by ID")
async def retrieve_payment(
    payment_id: Annotated[str, Field(description="The payment ID to retrieve")]
) -> Dict:
    """Retrieve payment details by ID"""
    return call_endpoint(f"/payments/{payment_id}", "GET")

@mcp.tool(name="delete_payment", description="Delete a payment")
async def delete_payment(
    payment_id: Annotated[str, Field(description="The payment ID to delete")]
) -> Dict:
    """Delete a payment by ID"""
    return call_endpoint(f"/payments/{payment_id}", "DELETE")

# ===== WEBHOOK ENDPOINTS =====

@mcp.tool(name="create_webhook", description="Create a webhook for event notifications")
async def create_webhook(
    webhook_type: Annotated[str, Field(description="Webhook event type (e.g., payment.update, entity.create)")],
    url: Annotated[str, Field(description="URL to receive webhook notifications")],
    auth_token: Annotated[Optional[str], Field(description="Authorization token for webhook security")] = None,
    hmac_secret: Annotated[Optional[str], Field(description="HMAC secret for webhook verification")] = None,
) -> Dict:
    """Create a webhook for receiving event notifications"""
    webhook_data = {
        "type": webhook_type,
        "url": url
    }
    if auth_token:
        webhook_data["auth_token"] = auth_token
    if hmac_secret:
        webhook_data["hmac_secret"] = hmac_secret
    
    return call_endpoint("/webhooks", "POST", data=webhook_data)

@mcp.tool(name="retrieve_webhook", description="Retrieve a specific webhook")
async def retrieve_webhook(
    webhook_id: Annotated[str, Field(description="The webhook ID to retrieve")]
) -> Dict:
    """Retrieve a webhook by ID"""
    return call_endpoint(f"/webhooks/{webhook_id}", "GET")

@mcp.tool(name="list_webhooks", description="List all webhooks")
async def list_webhooks() -> Dict:
    """List all registered webhooks"""
    return call_endpoint("/webhooks", "GET")

@mcp.tool(name="delete_webhook", description="Delete a webhook")
async def delete_webhook(
    webhook_id: Annotated[str, Field(description="The webhook ID to delete")]
) -> Dict:
    """Delete a webhook by ID"""
    return call_endpoint(f"/webhooks/{webhook_id}", "DELETE")

# ===== MERCHANT ENDPOINTS =====

@mcp.tool(name="list_merchants", description="List all merchants")
async def list_merchants() -> Dict:
    """List all merchants (financial institutions)"""
    return call_endpoint("/merchants", "GET")

@mcp.tool(name="retrieve_merchant", description="Retrieve a specific merchant")
async def retrieve_merchant(
    merchant_id: Annotated[str, Field(description="The merchant ID to retrieve")]
) -> Dict:
    """Retrieve merchant details by ID"""
    return call_endpoint(f"/merchants/{merchant_id}", "GET")

# ===== SUBSCRIPTION ENDPOINTS =====

@mcp.tool(name="create_entity_subscription", description="Create a subscription for an entity")
async def create_entity_subscription(
    entity_id: Annotated[str, Field(description="The entity ID")],
    subscription_type: Annotated[str, Field(description="Subscription type: credit_score, connect, or attribute")]
) -> Dict:
    """Create a subscription for continuous updates on an entity"""
    return call_endpoint(f"/entities/{entity_id}/subscriptions", "POST", data={"name": subscription_type})

@mcp.tool(name="retrieve_entity_subscription", description="Retrieve a specific entity subscription")
async def retrieve_entity_subscription(
    entity_id: Annotated[str, Field(description="The entity ID")],
    subscription_id: Annotated[str, Field(description="The subscription ID")]
) -> Dict:
    """Retrieve a specific subscription"""
    return call_endpoint(f"/entities/{entity_id}/subscriptions/{subscription_id}", "GET")

@mcp.tool(name="list_entity_subscriptions", description="List entity subscriptions")
async def list_entity_subscriptions(
    entity_id: Annotated[str, Field(description="The entity ID")]
) -> Dict:
    """List all subscriptions for an entity"""
    return call_endpoint(f"/entities/{entity_id}/subscriptions", "GET")

@mcp.tool(name="delete_entity_subscription", description="Delete an entity subscription")
async def delete_entity_subscription(
    entity_id: Annotated[str, Field(description="The entity ID")],
    subscription_id: Annotated[str, Field(description="The subscription ID to delete")]
) -> Dict:
    """Delete a subscription"""
    return call_endpoint(f"/entities/{entity_id}/subscriptions/{subscription_id}", "DELETE")

@mcp.tool(name="create_account_subscription", description="Create a subscription for an account")
async def create_account_subscription(
    account_id: Annotated[str, Field(description="The account ID")],
    subscription_type: Annotated[str, Field(description="Subscription type: update, transaction, or balance")]
) -> Dict:
    """Create a subscription for continuous updates on an account"""
    return call_endpoint(f"/accounts/{account_id}/subscriptions", "POST", data={"name": subscription_type})

@mcp.tool(name="list_account_subscriptions", description="List account subscriptions")
async def list_account_subscriptions(
    account_id: Annotated[str, Field(description="The account ID")]
) -> Dict:
    """List all subscriptions for an account"""
    return call_endpoint(f"/accounts/{account_id}/subscriptions", "GET")

@mcp.tool(name="delete_account_subscription", description="Delete an account subscription")
async def delete_account_subscription(
    account_id: Annotated[str, Field(description="The account ID")],
    subscription_id: Annotated[str, Field(description="The subscription ID to delete")]
) -> Dict:
    """Delete an account subscription"""
    return call_endpoint(f"/accounts/{account_id}/subscriptions/{subscription_id}", "DELETE")

def main():
    mcp.run(transport="streamable-http", port=8002)

if __name__ == "__main__":
    main()