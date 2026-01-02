from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field


Role = Literal["admin", "analyst", "support"]


class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=10)
    role: Role = "support"


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: str
    email: EmailStr
    role: Role


class TransactionCreateIn(BaseModel):
    amount_kobo: int = Field(ge=0)
    currency: str = "NGN"
    reference: str = Field(min_length=8, max_length=64)


class TransactionOut(BaseModel):
    id: str
    user_id: str
    amount_kobo: int
    currency: str
    reference: str


class TokenOut(BaseModel):
    token: str


class ApiError(BaseModel):
    error: str
    detail: Optional[str] = None

