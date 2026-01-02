from fastapi import APIRouter, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.security import create_access_token, hash_password, verify_password
from app.db import get_cursor
from app.models import LoginIn, RegisterIn, TokenOut, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])
limiter = Limiter(key_func=get_remote_address)


@router.post("/register", response_model=UserOut)
@limiter.limit("10/minute")
def register(request: Request, payload: RegisterIn):
    email = payload.email.lower()
    password_hash = hash_password(payload.password)
    try:
        with get_cursor() as cur:
            cur.execute(
                "insert into users (email, password_hash, role) values (%s, %s, %s) returning id, email, role",
                (email, password_hash, payload.role),
            )
            row = cur.fetchone()
            return row
    except Exception:
        raise HTTPException(status_code=409, detail="email_in_use")


@router.post("/login", response_model=TokenOut)
@limiter.limit("20/minute")
def login(request: Request, payload: LoginIn):
    email = payload.email.lower()
    with get_cursor() as cur:
        cur.execute(
            "select id, email, role, password_hash from users where email = %s",
            (email,),
        )
        user = cur.fetchone()

    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="invalid_credentials")

    token = create_access_token(user_id=str(user["id"]), email=user["email"], role=user["role"])
    return {"token": token}
