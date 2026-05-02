"""
API Integration Troubleshooting Lab

This application is a deliberately designed FastAPI service used to simulate
real-world API integration issues encountered in production environments.

Purpose
-------
The goal of this lab is to help engineers and technical support teams:

- Reproduce common API failures
- Diagnose integration issues
- Practice debugging workflows
- Build runbooks for recurring problems

What This App Simulates
-----------------------
1. Authentication failures (OAuth / Bearer token)
   - Missing Authorization header
   - Invalid or expired tokens

2. Payload validation errors
   - Missing required fields
   - Invalid data formats (e.g., email)
   - Business logic constraints

3. Webhook integration issues
   - Missing or invalid HMAC signature
   - Malformed JSON payloads
   - Unsupported event types

4. Data retrieval issues
   - Resource not found (404)
   - Unauthorized access

5. Performance / reliability problems
   - Slow endpoints (timeout simulation)
   - Retry scenarios

How It’s Used
-------------
- Used alongside client scripts to simulate real API interactions
- Paired with scenarios/ and runbooks/ to practice debugging
- Helps demonstrate API troubleshooting skills for:
  - Developer support roles
  - Data platform engineering
  - SaaS integration debugging

Important Notes
---------------
- Uses in-memory storage (not production-safe)
- Tokens and secrets are hardcoded for demo purposes
- Designed for local testing only

Run Locally
-----------
uvicorn src.app:app --reload

Then open:
http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import hmac
import hashlib
import time
import uuid


app = FastAPI(
    title="API Integration Troubleshooting Lab",
    description="A small API designed to reproduce and debug common integration failures.",
    version="1.0.0",
)

# Demo tokens/secrets for local troubleshooting only.
VALID_BEARER_TOKEN = "demo-valid-token"
WEBHOOK_SECRET = "demo-webhook-secret"

# In-memory storage for lab purposes.
ORDERS = {}


class OrderCreate(BaseModel):
    customer_email: EmailStr
    product_id: str = Field(..., min_length=3)
    quantity: int = Field(..., gt=0)
    notes: Optional[str] = None


class OrderResponse(BaseModel):
    order_id: str
    customer_email: str
    product_id: str
    quantity: int
    status: str
    created_at: float


def validate_bearer_token(authorization: Optional[str]) -> None:
    """
    Validate OAuth-style Bearer token.

    Expected header:
    Authorization: Bearer demo-valid-token
    """
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail={
                "error": "missing_authorization_header",
                "message": "Authorization header is required.",
            },
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail={
                "error": "invalid_authorization_scheme",
                "message": "Authorization header must use Bearer scheme.",
            },
        )

    token = authorization.replace("Bearer ", "").strip()

    if token != VALID_BEARER_TOKEN:
        raise HTTPException(
            status_code=401,
            detail={
                "error": "invalid_token",
                "message": "Bearer token is invalid or expired.",
            },
        )


def calculate_signature(payload: bytes) -> str:
    """
    Calculate HMAC SHA256 signature for webhook payload.
    """
    return hmac.new(
        WEBHOOK_SECRET.encode("utf-8"),
        payload,
        hashlib.sha256,
    ).hexdigest()


def validate_webhook_signature(payload: bytes, signature: Optional[str]) -> None:
    """
    Validate webhook signature.

    Expected header:
    X-Webhook-Signature: <hmac-sha256>
    """
    if not signature:
        raise HTTPException(
            status_code=401,
            detail={
                "error": "missing_webhook_signature",
                "message": "X-Webhook-Signature header is required.",
            },
        )

    expected_signature = calculate_signature(payload)

    if not hmac.compare_digest(signature, expected_signature):
        raise HTTPException(
            status_code=401,
            detail={
                "error": "invalid_webhook_signature",
                "message": "Webhook signature verification failed.",
            },
        )


@app.get("/health")
def health_check():
    """
    Basic health endpoint.
    """
    return {
        "status": "ok",
        "service": "api-integration-troubleshooting-lab",
    }


@app.post("/api/orders", response_model=OrderResponse, status_code=201)
def create_order(
    order: OrderCreate,
    authorization: Optional[str] = Header(default=None),
):
    """
    Create an order.

    Common troubleshooting scenarios:
    - Missing Authorization header
    - Invalid Bearer token
    - Missing required payload fields
    - Invalid email format
    - Quantity <= 0
    """
    validate_bearer_token(authorization)

    order_id = str(uuid.uuid4())

    record = {
        "order_id": order_id,
        "customer_email": order.customer_email,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "status": "created",
        "created_at": time.time(),
    }

    ORDERS[order_id] = record

    return record


@app.get("/api/orders/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: str,
    authorization: Optional[str] = Header(default=None),
):
    """
    Retrieve an order by ID.

    Common troubleshooting scenarios:
    - Invalid token
    - Order ID not found
    """
    validate_bearer_token(authorization)

    if order_id not in ORDERS:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "order_not_found",
                "message": f"Order {order_id} does not exist.",
            },
        )

    return ORDERS[order_id]


@app.post("/webhooks/payment")
async def payment_webhook(
    request: Request,
    x_webhook_signature: Optional[str] = Header(default=None),
):
    """
    Receive a payment webhook.

    Common troubleshooting scenarios:
    - Missing signature
    - Invalid signature
    - Malformed JSON payload
    - Unknown event type
    """
    payload = await request.body()

    validate_webhook_signature(payload, x_webhook_signature)

    try:
        event = await request.json()
    except Exception:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "invalid_json",
                "message": "Webhook payload must be valid JSON.",
            },
        )

    event_type = event.get("type")
    order_id = event.get("order_id")

    if event_type not in ["payment.succeeded", "payment.failed"]:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "unsupported_event_type",
                "message": f"Unsupported event type: {event_type}",
            },
        )

    if order_id and order_id in ORDERS:
        if event_type == "payment.succeeded":
            ORDERS[order_id]["status"] = "paid"
        elif event_type == "payment.failed":
            ORDERS[order_id]["status"] = "payment_failed"

    return {
        "received": True,
        "event_type": event_type,
        "order_id": order_id,
    }


@app.get("/api/slow")
def slow_endpoint(
    delay: int = 3,
    authorization: Optional[str] = Header(default=None),
):
    """
    Simulate a slow API response for timeout/retry troubleshooting.

    Example:
    /api/slow?delay=5
    """
    validate_bearer_token(authorization)

    if delay > 10:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "delay_too_large",
                "message": "Delay must be 10 seconds or less.",
            },
        )

    time.sleep(delay)

    return {
        "status": "completed",
        "delay_seconds": delay,
    }