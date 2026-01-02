# FinGuard API (Demo / Case Study)

FinGuard API is a **FastAPI + PostgreSQL** reference backend designed to demonstrate:
- **JWT authentication**
- **role-based access control (RBAC)**
- **schema-first SQL migrations**
- **structured, security-aware engineering**

This is a **demo project** (not a claim of past client work).

## Features

- Register/login endpoints (demo-friendly)
- `/me` endpoint (authenticated)
- Admin-only user listing
- “Transaction-like” resource endpoints (create/list) to show typical fintech patterns
- Docker-friendly Postgres setup

## Threat model (high level)

**Primary assets**
- Credentials + JWT secrets
- User roles/permissions (authorization integrity)
- Transaction-like records (integrity and confidentiality)

**Attack surfaces**
- Auth endpoints (brute force, credential stuffing, enumeration)
- Business endpoints (IDOR, missing access control, abuse via automation)
- Logging layer (PII leakage)
- DB (SQL injection, excessive privileges)

**Abuse cases → mitigations (examples)**
- Credential stuffing → rate limiting, consistent errors, optional account lockouts
- JWT abuse (stolen token) → short-lived tokens, rotation strategy (future), TLS-only deployment
- Enumeration → generic login/register errors, pagination, access checks
- Injection → parameterized queries, strict validation
- PII leakage via logs → avoid logging payloads/secrets, structured logs with redaction

## Run locally

### 1) Start Postgres
`docker compose up -d db`

### 2) Create venv + install deps
`python -m venv .venv`
`.\.venv\Scripts\activate`
`pip install -r requirements.txt`

### 3) Configure env
Copy `.env.example` → `.env` and update values.

### 4) Apply migrations
`python scripts/migrate.py`

### 5) Start API
`uvicorn app.main:app --reload --port 8000`

Open docs: `http://localhost:8000/docs`

## Security considerations (implementation notes)

- Passwords are hashed with bcrypt via `passlib`.
- JWT tokens are short-lived; store them securely (avoid localStorage in production).
- RBAC is enforced on the API routes (not just UI).
- Rate limiting is enabled for auth endpoints (demo defaults).
- Errors avoid leaking internals; logs should not include secrets/PII.

