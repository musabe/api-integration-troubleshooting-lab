# 🔌 API Integration Troubleshooting Lab

> A hands-on FastAPI lab that reproduces real-world API integration failures — including authentication issues, payload validation errors, webhook signature problems, and timeout scenarios — with a client script to simulate and debug each case.

![CI](https://github.com/musabe/api-integration-troubleshooting-lab/actions/workflows/ci.yml/badge.svg)
![Language](https://img.shields.io/badge/language-Python-blue?style=flat-square)
![Framework](https://img.shields.io/badge/framework-FastAPI-green?style=flat-square)
![Status](https://img.shields.io/badge/status-active-brightgreen?style=flat-square)

---

## 🎯 Overview

This project simulates a real-world API used in SaaS integrations and provides a controlled environment to reproduce and diagnose common integration failures.

It is designed for:

- Developer Support Engineers
- API / Integration Engineers
- Technical Support teams

The goal is to practice debugging workflows and build repeatable troubleshooting runbooks, including production-style guides for authentication, payload validation, webhook failures, and idempotency handling.

---

## 💡 Why This Project Exists

API integrations often fail due to subtle issues that are difficult to debug quickly.

Common problems include:

- Missing or invalid authentication tokens
- Incorrect payload structure or data types
- Webhook signature validation failures
- Timeouts and retry issues
- Misconfigured clients

This lab shifts debugging **left** by letting you:

- Reproduce failures in a controlled environment
- Understand API behavior under error conditions
- Build repeatable troubleshooting workflows

---

## 🧰 Tech Stack

- **Language** — Python 3.8+
- **Framework** — FastAPI
- **HTTP Client** — requests
- **Validation** — Pydantic
- **Server** — Uvicorn

---

## 📁 Project Structure

```
api-integration-troubleshooting-lab/
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
│   ├── api-error-troubleshooting.md
│   ├── oauth-debugging.md
│   └── webhook-debugging.md
├── examples/
│   ├── sample-api-errors.md
│   ├── sample_error_response.json
│   └── sample_payload.json
├── runbooks/
│   ├── api_error_troubleshooting.md
│   ├── idempotency_debugging_runbook.md
│   ├── oauth_debugging_runbook.md
│   └── webhook_debugging_runbook.md
├── scenarios/
│   ├── duplicate_webhook_idempotency_failure.md
│   ├── oauth_invalid_token.md
│   ├── payload_validation_error.md
│   ├── timeout_retry_issue.md
│   └── webhook_signature_failure.md
├── src/
│   ├── __init__.py
│   ├── app.py              # FastAPI service with failure scenarios
│   ├── client.py           # Client script to reproduce issues
│   ├── config.py
│   └── logger.py
├── tests/
│   ├── test_api.py
│   └── test_placeholder.py
├── pytest.ini
├── README.md
└── requirements.txt
```

---

## 🚀 Getting Started

### ✅ Prerequisites

- Python 3.8+
- pip installed

### ▶️ Step 1 — Install dependencies

```bash
pip install -r requirements.txt
```

### ▶️ Step 2 — Start the API

```bash
uvicorn src.app:app --reload
```

Open the interactive docs at:

```
http://127.0.0.1:8000/docs
```

### ▶️ Step 3 — Run the client

```bash
python src/client.py
```

---

## 🔍 What It Simulates

| Scenario | Trigger | Response |
|---|---|---|
| Missing `Authorization` header | No auth | `401` |
| Invalid Bearer token | Bad token | `401` |
| Valid Bearer token | Correct token | `201` |
| Missing required fields | Bad payload | `422` |
| Invalid email format | Bad email | `422` |
| Missing webhook signature | No header | `401` |
| Invalid webhook signature | Wrong hash | `401` |
| Resource not found | Bad ID | `404` |
| Duplicate webhook / idempotency | Same event sent twice | Safe skip (`duplicate=true`) |
| Slow endpoint / timeout | Delay injection | Client timeout |

---

## 📚 Runbooks

This project includes structured troubleshooting runbooks for common API failures:

- [Webhook Signature Debugging](runbooks/webhook_debugging_runbook.md)
- [OAuth / Bearer Token Debugging](runbooks/oauth_debugging_runbook.md)
- [Payload Validation Error Debugging](runbooks/api_error_troubleshooting.md)
- [Duplicate Webhook / Idempotency](runbooks/idempotency_debugging_runbook.md)

Each runbook provides:

- Step-by-step debugging workflow
- Root cause analysis guidance
- Reproduction steps using the client
- Practical resolution checklist

👉 These reflect real-world support and developer troubleshooting processes.

---

## 📤 Example Output

Running `python src/client.py` produces:

```
--- Missing Authorization header ---
HTTP 401

--- Invalid Bearer token ---
HTTP 401

--- Valid Bearer token ---
HTTP 201

--- Invalid email format ---
HTTP 422

--- Missing webhook signature ---
HTTP 401

--- Valid webhook signature ---
HTTP 200

--- Slow endpoint ---
Client-side timeout occurred
```

---

## 🧠 Design Approach

- Failures are intentional and reproducible
- Error responses are structured and descriptive
- Client simulates real-world API usage
- Designed for debugging, not production use
- In-memory storage for simplicity

---

## ✅ CI Status

This project includes a GitHub Actions pipeline that:

- Installs dependencies
- Runs API tests using pytest
- Validates authentication, validation, and webhook scenarios

All tests must pass before changes are considered valid.

---

## 🚧 Status

| Feature | Status |
|---|---|
| FastAPI service | ✅ Done |
| OAuth simulation | ✅ Done |
| Payload validation scenarios | ✅ Done |
| Webhook simulation | ✅ Done |
| Timeout / retry scenarios | ✅ Done |
| Client script | ✅ Done |
| Runbooks | ✅ Core Runbooks Complete |
| Retry logic with backoff | 🔜 Planned |
| Rate limiting / 429 scenarios | 🔜 Planned |
| Docker support | 🔜 Planned |

---

## 🔧 How This Maps to Real Systems

The scenarios in this lab reflect common failures seen in:

- Stripe / payment webhooks
- GitHub / GitLab integrations
- SaaS API integrations
- API gateway authentication flows
- Partner onboarding environments

This makes the lab directly applicable to real production debugging scenarios.

---

## 👤 Author

**Mustapha Abella**  
Senior Technical Support Engineer  
Focused on API-driven SaaS, data integration, and developer-facing support  

[github.com/musabe](https://github.com/musabe)
