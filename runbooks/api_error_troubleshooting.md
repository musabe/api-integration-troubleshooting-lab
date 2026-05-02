# Runbook: Debugging Payload Validation Errors

## 🎯 Objective

Identify and resolve API requests failing with payload validation errors, commonly returned as:

```text
HTTP 422 - Unprocessable Entity

🔍 Step 1 — Confirm the Error

Typical response:

{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "customer_email"],
      "msg": "Field required"
    }
  ]
}

This means the API received the request, but the JSON body did not match the expected schema.

🔍 Step 2 — Identify the Failing Field

Look at:

loc

Example:

"loc": ["body", "customer_email"]

This means:

customer_email is missing or invalid
🔍 Step 3 — Identify the Validation Type

Common examples:

Error Type	Meaning	Example Fix
missing	Required field missing	Add the field
value_error	Invalid field value	Correct format
greater_than	Number too small	Use value greater than minimum
string_too_short	String too short	Provide longer value
🔍 Step 4 — Compare Against Expected Payload

Expected payload:

{
  "customer_email": "customer@example.com",
  "product_id": "SKU-001",
  "quantity": 1
}

Required fields:

customer_email
product_id
quantity

Rules:

customer_email must be valid email format
product_id must be at least 3 characters
quantity must be greater than 0
🔍 Step 5 — Reproduce Locally

Start the API:

uvicorn src.app:app --reload

Run:

python src/client.py

Confirm:

Missing required field → 422
Invalid email format → 422
Invalid quantity → 422
🔍 Step 6 — Test Manually with curl

Missing email:

curl -X POST http://127.0.0.1:8000/api/orders \
  -H "Authorization: Bearer demo-valid-token" \
  -H "Content-Type: application/json" \
  -d "{\"product_id\":\"SKU-001\",\"quantity\":1}"

Invalid email:

curl -X POST http://127.0.0.1:8000/api/orders \
  -H "Authorization: Bearer demo-valid-token" \
  -H "Content-Type: application/json" \
  -d "{\"customer_email\":\"not-an-email\",\"product_id\":\"SKU-001\",\"quantity\":1}"

Invalid quantity:

curl -X POST http://127.0.0.1:8000/api/orders \
  -H "Authorization: Bearer demo-valid-token" \
  -H "Content-Type: application/json" \
  -d "{\"customer_email\":\"test@example.com\",\"product_id\":\"SKU-001\",\"quantity\":0}"
✅ Resolution Checklist
 Request body is valid JSON
 Content-Type is application/json
 Required fields are present
 Field names match API schema exactly
 Email value is valid
 Quantity is greater than 0
 Payload matches API documentation
🧠 Root Cause Summary

Payload validation failures usually come from:

👉 Missing fields
👉 Invalid field formats
👉 Wrong data types
👉 Values outside allowed limits

Start debugging with the detail.loc and detail.msg fields.

🧩 Real-World Context

This issue is commonly encountered in:

API onboarding
Partner integrations
Postman testing
Webhook/event payloads
SaaS platform integrations