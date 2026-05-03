# Runbook: Debugging Duplicate Webhook Processing / Idempotency Failures

## 🎯 Objective

Identify and resolve cases where the same webhook event is processed more than once.

---

## 🔍 Step 1 — Confirm Duplicate Processing

Check API logs for repeated processing of the same order or event:

```text
[DEBUG] Processing payment.succeeded for <order_id>
[DEBUG] Processing payment.succeeded for <order_id>
```

This indicates that the same webhook was accepted and processed more than once.

---

## 🔍 Step 2 — Confirm Whether the Webhook Has a Unique Event ID

Check the webhook payload. Expected:

```json
{
  "event_id": "evt_123",
  "type": "payment.succeeded",
  "order_id": "order_123"
}
```

If no `event_id` or idempotency key exists, duplicate detection is unreliable.

---

## 🔍 Step 3 — Check Current Handler Behavior

**Current unsafe behavior:**

```
validate signature
process event
return 200
```

**Safe behavior should be:**

```
validate signature
check event_id
skip if already processed
process if new
record event_id
return 200
```

---

## 🔍 Step 4 — Reproduce Locally

Start the API:

```bash
uvicorn src.app:app --reload
```

Run the client:

```bash
python src/client.py
```

Confirm that the client sends:

- Valid webhook signature
- Duplicate webhook (should not reprocess)

---

## 🔍 Step 5 — Validate Impact

Check whether duplicate processing caused:

- Duplicate state transitions
- Duplicate downstream actions
- Duplicate notifications
- Incorrect audit entries
- Confusing customer-facing behavior

---

## ✅ Resolution Checklist

- [ ] Webhook payload contains a unique `event_id`
- [ ] API stores processed event IDs
- [ ] Duplicate events are safely skipped
- [ ] Duplicate webhook still returns `200`
- [ ] Logs clearly identify duplicate events
- [ ] Tests cover duplicate webhook behavior

---

## 🧠 Root Cause Summary

Webhook providers may deliver the same event more than once — this is expected behavior. The API must treat webhook handling as idempotent by tracking processed event IDs and safely skipping duplicates.

---

## 🧩 Real-World Context

Duplicate webhook delivery is common in:

- Stripe
- GitHub
- GitLab
- Payment gateways
- SaaS event platforms

Reliable webhook consumers must handle duplicate events safely.
