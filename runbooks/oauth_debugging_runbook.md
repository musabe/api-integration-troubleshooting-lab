# Runbook: Debugging OAuth / Bearer Token Failures

## 🎯 Objective

Identify and resolve API requests failing because of missing, malformed, invalid, or expired Bearer tokens.

---

## 🔍 Step 1 — Confirm the Error

Common responses:

```text
HTTP 401 - missing_authorization_header
HTTP 401 - invalid_authorization_scheme
HTTP 401 - invalid_token
```

Example response:

```json
{
  "detail": {
    "error": "invalid_token",
    "message": "Bearer token is invalid or expired."
  }
}
```

---

## 🔍 Step 2 — Check the Authorization Header

Expected format:

```
Authorization: Bearer demo-valid-token
```

Common mistakes:

- Missing `Authorization` header
- Typo in `Bearer`
- Extra spaces
- Token passed in body instead of header
- Token passed as query parameter
- Wrong casing or malformed header

---

## 🔍 Step 3 — Validate Token Value

Confirm the token matches the expected value.

For this lab:

```
demo-valid-token
```

Invalid example:

```
demo-invalid-token
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

Confirm:

- Missing token → `401`
- Invalid token → `401`
- Valid token → `201`

---

## 🔍 Step 5 — Test Manually with curl

**Missing token:**

```bash
curl -X POST http://127.0.0.1:8000/api/orders \
  -H "Content-Type: application/json" \
  -d '{"customer_email":"test@example.com","product_id":"SKU-001","quantity":1}'
```

**Invalid token:**

```bash
curl -X POST http://127.0.0.1:8000/api/orders \
  -H "Authorization: Bearer demo-invalid-token" \
  -H "Content-Type: application/json" \
  -d '{"customer_email":"test@example.com","product_id":"SKU-001","quantity":1}'
```

**Valid token:**

```bash
curl -X POST http://127.0.0.1:8000/api/orders \
  -H "Authorization: Bearer demo-valid-token" \
  -H "Content-Type: application/json" \
  -d '{"customer_email":"test@example.com","product_id":"SKU-001","quantity":1}'
```

---

## ✅ Resolution Checklist

- [ ] `Authorization` header is present
- [ ] Header uses `Bearer` scheme
- [ ] Token is not empty
- [ ] Token value is correct
- [ ] Token is sent in the header, not body or query string
- [ ] Client is calling the correct environment / API base URL

---

## 🧠 Root Cause Summary

Bearer token failures usually come from:

👉 Missing header  
👉 Wrong token  
👉 Malformed `Authorization` header  
👉 Wrong environment  

Start debugging with the request headers first.

---

## 🧩 Real-World Context

This issue is commonly encountered in:

- OAuth-protected SaaS APIs
- API gateway integrations
- Partner integrations
- Postman / curl testing
- Customer onboarding flows
