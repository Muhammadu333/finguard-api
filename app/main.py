from dotenv import load_dotenv
from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.routes.auth import limiter as auth_limiter
from app.api.routes.auth import router as auth_router
from app.api.routes.transactions import router as transactions_router
from app.api.routes.users import router as users_router

load_dotenv()

app = FastAPI(title="FinGuard API (Demo)")

app.state.limiter = auth_limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(transactions_router)

@app.get("/")
def root():
    return {
        "name": "finguard-api",
        "ok": True,
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "auth": { "register": "/auth/register", "login": "/auth/login" },
            "me": "/me",
            "admin_users": "/admin/users",
            "transactions": "/transactions",
        },
    }


@app.get("/health")
def health():
    return {"ok": True}
