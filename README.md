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

The goal is to practice debugging workflows and build repeatable troubleshooting runbooks.

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
├── src/
│   ├── app.py              # FastAPI service with failure scenarios
│   ├── client.py           # Client script to reproduce issues
│   ├── config.py
│   └── logger.py
├── scenarios/
│   ├── oauth_invalid_token.md
│   ├── webhook_signature_failure.md
│   ├── payload_validation_error.md
│   └── timeout_retry_issue.md
├── runbooks/
│   ├── oauth_debugging_runbook.md
│   ├── webhook_debugging_runbook.md
│   └── api_error_troubleshooting.md
├── tests/
├── examples/
│   ├── sample_payload.json
│   └── sample_error_response.json
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
| Slow endpoint / timeout | Delay injection | Client timeout |

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

![CI](https://github.com/musabe/api-integration-troubleshooting-lab/actions/workflows/ci.yml/badge.svg)

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
| Runbooks | 🔄 In Progress |
| Retry logic with backoff | 🔜 Planned |
| Rate limiting / 429 scenarios | 🔜 Planned |
| Docker support | 🔜 Planned |

---

## 👤 Author

**Mustapha Abella**
Senior Technical Support Engineer
Focused on API-driven SaaS, data integration, and developer-facing support

[github.com/musabe](https://github.com/musabe)
