from datetime import datetime, timedelta, timezone
from typing import Literal, TypedDict

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


Role = Literal["admin", "analyst", "support"]


class JwtClaims(TypedDict):
    sub: str
    email: str
    role: Role
    iss: str
    aud: str
    exp: int


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def create_access_token(*, user_id: str, email: str, role: Role) -> str:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=20)
    payload: JwtClaims = {
        "sub": user_id,
        "email": email,
        "role": role,
        "iss": settings.jwt_issuer,
        "aud": settings.jwt_audience,
        "exp": int(exp.timestamp()),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


def decode_access_token(token: str) -> JwtClaims:
    return jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=["HS256"],
        issuer=settings.jwt_issuer,
        audience=settings.jwt_audience,
    )

