import hashlib
import hmac
import json

from fastapi.testclient import TestClient

from src.app import app, WEBHOOK_SECRET


client = TestClient(app)


def build_signature(payload: dict) -> str:
    payload_bytes = json.dumps(payload).encode("utf-8")

    return hmac.new(
        WEBHOOK_SECRET.encode("utf-8"),
        payload_bytes,
        hashlib.sha256,
    ).hexdigest()


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_order_requires_authorization_header():
    response = client.post(
        "/api/orders",
        json={
            "customer_email": "test@example.com",
            "product_id": "SKU-001",
            "quantity": 1,
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"]["error"] == "missing_authorization_header"


def test_create_order_rejects_invalid_token():
    response = client.post(
        "/api/orders",
        headers={"Authorization": "Bearer invalid-token"},
        json={
            "customer_email": "test@example.com",
            "product_id": "SKU-001",
            "quantity": 1,
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"]["error"] == "invalid_token"


def test_create_order_accepts_valid_token():
    response = client.post(
        "/api/orders",
        headers={"Authorization": "Bearer demo-valid-token"},
        json={
            "customer_email": "test@example.com",
            "product_id": "SKU-001",
            "quantity": 1,
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["customer_email"] == "test@example.com"
    assert body["product_id"] == "SKU-001"
    assert body["quantity"] == 1
    assert body["status"] == "created"
    assert "order_id" in body


def test_payload_validation_missing_email():
    response = client.post(
        "/api/orders",
        headers={"Authorization": "Bearer demo-valid-token"},
        json={
            "product_id": "SKU-001",
            "quantity": 1,
        },
    )

    assert response.status_code == 422


def test_payload_validation_invalid_quantity():
    response = client.post(
        "/api/orders",
        headers={"Authorization": "Bearer demo-valid-token"},
        json={
            "customer_email": "test@example.com",
            "product_id": "SKU-001",
            "quantity": 0,
        },
    )

    assert response.status_code == 422


def test_get_order_not_found():
    response = client.get(
        "/api/orders/not-found",
        headers={"Authorization": "Bearer demo-valid-token"},
    )

    assert response.status_code == 404
    assert response.json()["detail"]["error"] == "order_not_found"


def test_webhook_requires_signature():
    payload = {
        "type": "payment.succeeded",
        "order_id": "demo-order-id",
    }

    response = client.post(
        "/webhooks/payment",
        json=payload,
    )

    assert response.status_code == 401
    assert response.json()["detail"]["error"] == "missing_webhook_signature"


def test_webhook_rejects_invalid_signature():
    payload = {
        "type": "payment.succeeded",
        "order_id": "demo-order-id",
    }

    response = client.post(
        "/webhooks/payment",
        headers={"X-Webhook-Signature": "invalid-signature"},
        json=payload,
    )

    assert response.status_code == 401
    assert response.json()["detail"]["error"] == "invalid_webhook_signature"


def test_webhook_accepts_valid_signature():
    payload = {
        "type": "payment.succeeded",
        "order_id": "demo-order-id",
    }

    signature = build_signature(payload)

    response = client.post(
        "/webhooks/payment",
        headers={"X-Webhook-Signature": signature},
        data=json.dumps(payload),
    )

    assert response.status_code == 200
    assert response.json()["received"] is True
    assert response.json()["event_type"] == "payment.succeeded"


def test_slow_endpoint_rejects_large_delay():
    response = client.get(
        "/api/slow?delay=11",
        headers={"Authorization": "Bearer demo-valid-token"},
    )

    assert response.status_code == 400
    assert response.json()["detail"]["error"] == "delay_too_large"