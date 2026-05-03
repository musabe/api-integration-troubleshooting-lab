# Scenario: Duplicate Webhook / Missing Idempotency

## Problem

A payment webhook can be delivered more than once. Without idempotency protection, the API processes the same event multiple times.

This can lead to:

- Duplicate state transitions
- Duplicate downstream actions
- Incorrect audit trails
- Customer confusion
- Potential double-processing in real systems

---

## Symptoms

When the same valid webhook is sent twice, the API logs show repeated processing:

```text
[DEBUG] Processing payment.succeeded for <order_id>
[DEBUG] Processing payment.succeeded for <order_id>
```

The response may still return:

```
HTTP 200
```

This makes the bug dangerous because the duplicate processing may appear successful.

---

## Root Cause

The webhook handler validates the signature but does not check whether the event has already been processed.

**Current behavior:**

```
valid signature → process event
duplicate valid signature → process event again
```

**Missing behavior:**

```
valid signature → check event_id/idempotency key → process only once
```

---

## How to Reproduce

### 1. Start the API

```bash
uvicorn src.app:app --reload
```

### 2. Run the client

```bash
python src/client.py
```

### 3. Observe duplicate webhook processing

The client sends the same webhook twice:

- Valid webhook signature
- Duplicate webhook (should not reprocess)

The server logs show that the same event is processed multiple times.

---

## Expected Behavior

The API should process a webhook event only once. A duplicate event should return a safe response such as:

```json
{
  "received": true,
  "duplicate": true,
  "message": "Webhook event already processed."
}
```

---

## Fix Strategy

Add an idempotency key or event ID to webhook payloads and track processed events.

**Example payload:**

```json
{
  "event_id": "evt_123",
  "type": "payment.succeeded",
  "order_id": "order_123"
}
```

**Processing logic:**

```
if event_id already processed:
    skip processing
else:
    process event
    mark event_id as processed
```

---

## Real-World Context

Most webhook providers retry delivery when they do not receive a timely success response.

Examples:

- Stripe webhooks
- GitHub webhooks
- Payment gateways
- SaaS event systems

Webhook consumers must be idempotent because duplicate delivery is normal behavior, not an exception.
