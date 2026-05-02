# Runbook: Debugging Webhook Signature Failures

## 🎯 Objective

Identify and resolve webhook requests failing with:

```
HTTP 401 - invalid_webhook_signature
```

---

## 🔍 Step 1 — Confirm the Error

Check the API response:

```json
{
  "detail": {
    "error": "invalid_webhook_signature",
    "message": "Webhook signature verification failed."
  }
}
```

---

## 🔍 Step 2 — Verify Webhook Secret

Confirm both systems use the same secret:

- API server (`WEBHOOK_SECRET`)
- Client / sender

Check for:

- Leading/trailing spaces
- Incorrect environment variables
- Wrong secret in config files

---

## 🔍 Step 3 — Inspect Payload Integrity

Compare:

- Payload used to generate signature
- Payload received by API

Look for differences in:

- Field order
- Whitespace
- Extra/missing fields

---

## 🔍 Step 4 — Validate Encoding

**Correct:**

```python
payload_bytes = json.dumps(payload).encode("utf-8")
```

**Incorrect:**

```python
str(payload)
```

---

## 🔍 Step 5 — Recompute Signature

Run locally:

```python
import hmac, hashlib
hmac.new(secret.encode(), payload_bytes, hashlib.sha256).hexdigest()
```

Compare with header:

```
X-Webhook-Signature
```

---

## 🔍 Step 6 — Check for Middleware Changes

Verify that no layer modifies the payload:

- API gateway
- Reverse proxy
- Logging middleware
- Serialization layers

---

## 🔍 Step 7 — Reproduce Locally

Run:

```bash
python src/client.py
```

Confirm:

- Invalid signature → `401`
- Valid signature → `200`

---

## ✅ Resolution Checklist

- [ ] Secret matches on both sides
- [ ] Payload is identical when signed and sent
- [ ] Encoding is UTF-8
- [ ] Signature recomputation matches header
- [ ] No middleware altering request

---

## 🧠 Root Cause Summary

Webhook signature failures are almost always caused by:

👉 Payload mismatch  
👉 Incorrect secret  

Start debugging there first.

---

## 🧩 Real-World Context

This issue is commonly encountered in:

- Stripe webhooks
- GitHub webhooks
- Payment gateways
- SaaS event-driven systems

It is one of the most frequent causes of webhook integration failures in production.