from fastapi import Header, HTTPException

from app.core.security import decode_access_token


def get_bearer_token(authorization: str | None = Header(default=None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="unauthorized")
    return authorization[7:]


def get_current_user(authorization: str | None = Header(default=None)):
    token = get_bearer_token(authorization)
    try:
        return decode_access_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="unauthorized")


def require_role(allowed: set[str]):
    def checker(authorization: str | None = Header(default=None)):
        user = get_current_user(authorization)
        if user["role"] not in allowed:
            raise HTTPException(status_code=403, detail="forbidden")
        return user

    return checker

