"""
API Integration Troubleshooting Lab — Client Script

This client is used to exercise the FastAPI demo service in `src/app.py`.

Purpose
-------
The goal of this script is to reproduce common API integration failures in a
controlled local environment so they can be diagnosed and documented.

What This Client Tests
----------------------
1. Health check
   - Confirms the API is reachable

2. OAuth / Bearer token failures
   - Missing Authorization header
   - Invalid Bearer token
   - Valid Bearer token

3. Payload validation failures
   - Missing required fields
   - Invalid email format
   - Invalid quantity

4. Webhook signature failures
   - Missing webhook signature
   - Invalid webhook signature
   - Valid webhook signature

5. Timeout / retry scenarios
   - Calls a deliberately slow endpoint
   - Demonstrates timeout handling from the client side

How It's Used
-------------
1. Start the API:
   uvicorn src.app:app --reload

2. Run this client:
   python src/client.py

This script prints each request, response status code, and response body so the
user can observe symptoms and map them to troubleshooting runbooks.

Important Notes
---------------
- This is a local troubleshooting tool, not a production client.
- Tokens and secrets match the demo values in `src/app.py`.
- The script intentionally sends bad requests to reproduce failure scenarios.
"""

import hashlib
import hmac
import json
from typing import Any, Dict, Optional

import requests


BASE_URL = "http://127.0.0.1:8000"
VALID_BEARER_TOKEN = "demo-valid-token"
INVALID_BEARER_TOKEN = "demo-invalid-token"
WEBHOOK_SECRET = "demo-webhook-secret"


def print_section(title: str) -> None:
    """
    Print a readable section header.
    """
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def print_response(label: str, response: requests.Response) -> None:
    """
    Print response details in a support-friendly format.
    """
    print(f"\n--- {label} ---")
    print(f"HTTP {response.status_code}")

    try:
        print(json.dumps(response.json(), indent=2))
    except ValueError:
        print(response.text)


def auth_headers(token: Optional[str] = VALID_BEARER_TOKEN) -> Dict[str, str]:
    """
    Build Authorization header.

    If token is None, return no Authorization header to simulate
    a missing-token failure.
    """
    if token is None:
        return {}

    return {
        "Authorization": f"Bearer {token}",
    }


def webhook_signature(payload: Dict[str, Any], secret: str = WEBHOOK_SECRET) -> str:
    """
    Generate HMAC SHA256 signature for webhook payload.

    The signature must be calculated from the exact JSON bytes sent to the API.
    """
    payload_bytes = json.dumps(payload).encode("utf-8")

    return hmac.new(
        secret.encode("utf-8"),
        payload_bytes,
        hashlib.sha256,
    ).hexdigest()


def health_check() -> None:
    """
    Test API reachability.
    """
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    print_response("Health check", response)


def create_order(
    payload: Dict[str, Any],
    token: Optional[str] = VALID_BEARER_TOKEN,
    label: str = "Create order",
) -> Optional[str]:
    """
    Call POST /api/orders.

    Returns order_id when successful.
    """
    headers = {
        **auth_headers(token),
        "Content-Type": "application/json",
    }

    response = requests.post(
        f"{BASE_URL}/api/orders",
        headers=headers,
        json=payload,
        timeout=5,
    )

    print_response(label, response)

    if response.status_code == 201:
        return response.json().get("order_id")

    return None


def get_order(order_id: str, token: Optional[str] = VALID_BEARER_TOKEN) -> None:
    """
    Call GET /api/orders/{order_id}.
    """
    response = requests.get(
        f"{BASE_URL}/api/orders/{order_id}",
        headers=auth_headers(token),
        timeout=5,
    )

    print_response(f"Get order {order_id}", response)


def send_payment_webhook(
    payload: Dict[str, Any],
    signature: Optional[str],
    label: str,
) -> None:
    """
    Call POST /webhooks/payment.

    Signature scenarios:
    - None = missing signature
    - invalid string = invalid signature
    - valid HMAC = success
    """
    headers = {
        "Content-Type": "application/json",
    }

    if signature is not None:
        headers["X-Webhook-Signature"] = signature

    response = requests.post(
        f"{BASE_URL}/webhooks/payment",
        headers=headers,
        data=json.dumps(payload),
        timeout=5,
    )

    print_response(label, response)


def call_slow_endpoint(delay: int, timeout: int) -> None:
    """
    Call slow endpoint to reproduce client-side timeout behavior.
    """
    try:
        response = requests.get(
            f"{BASE_URL}/api/slow",
            params={"delay": delay},
            headers=auth_headers(),
            timeout=timeout,
        )
        print_response(f"Slow endpoint delay={delay}, timeout={timeout}", response)

    except requests.exceptions.Timeout:
        print(f"\n--- Slow endpoint delay={delay}, timeout={timeout} ---")
        print("Client-side timeout occurred.")
        print(
            "Troubleshooting hint: compare client timeout with server response delay."
        )


def run_oauth_scenarios() -> None:
    """
    Reproduce common OAuth / Bearer token failures.
    """
    print_section("OAuth / Bearer Token Scenarios")

    valid_payload = {
        "customer_email": "customer@example.com",
        "product_id": "SKU-001",
        "quantity": 1,
    }

    create_order(
        valid_payload,
        token=None,
        label="Missing Authorization header",
    )

    create_order(
        valid_payload,
        token=INVALID_BEARER_TOKEN,
        label="Invalid Bearer token",
    )

    create_order(
        valid_payload,
        token=VALID_BEARER_TOKEN,
        label="Valid Bearer token",
    )


def run_payload_validation_scenarios() -> None:
    """
    Reproduce common payload validation failures.
    """
    print_section("Payload Validation Scenarios")

    create_order(
        {
            "product_id": "SKU-001",
            "quantity": 1,
        },
        label="Missing required field: customer_email",
    )

    create_order(
        {
            "customer_email": "not-an-email",
            "product_id": "SKU-001",
            "quantity": 1,
        },
        label="Invalid email format",
    )

    create_order(
        {
            "customer_email": "customer@example.com",
            "product_id": "SKU-001",
            "quantity": 0,
        },
        label="Invalid quantity",
    )


def run_webhook_scenarios(order_id: Optional[str]) -> None:
    """
    Reproduce webhook signature validation failures and a successful webhook.
    """
    print_section("Webhook Signature Scenarios")

    payload = {
        "type": "payment.succeeded",
        "order_id": order_id or "missing-order-id",
    }

    send_payment_webhook(
        payload,
        signature=None,
        label="Missing webhook signature",
    )

    send_payment_webhook(
        payload,
        signature="invalid-signature",
        label="Invalid webhook signature",
    )

    valid_signature = webhook_signature(payload)

    send_payment_webhook(
        payload,
        signature=valid_signature,
        label="Valid webhook signature",
    )

    # Duplicate webhook (simulate retry / re-delivery)
    send_payment_webhook(
        payload,
        signature=valid_signature,
        label="Duplicate webhook (should not reprocess)",
    )


def run_timeout_scenarios() -> None:
    """
    Reproduce timeout and retry-related behavior.
    """
    print_section("Timeout / Retry Scenarios")

    call_slow_endpoint(delay=2, timeout=5)
    call_slow_endpoint(delay=5, timeout=2)


def main() -> None:
    """
    Run all troubleshooting scenarios.
    """
    print_section("API Integration Troubleshooting Lab Client")

    health_check()

    run_oauth_scenarios()
    run_payload_validation_scenarios()

    print_section("Create Valid Order For Webhook Test")

    valid_order_payload = {
        "customer_email": "webhook.customer@example.com",
        "product_id": "SKU-999",
        "quantity": 2,
    }

    order_id = create_order(
        valid_order_payload,
        token=VALID_BEARER_TOKEN,
        label="Create order for webhook scenario",
    )

    if order_id:
        get_order(order_id)

    run_webhook_scenarios(order_id)

    if order_id:
        get_order(order_id)

    run_timeout_scenarios()


if __name__ == "__main__":
    main()
