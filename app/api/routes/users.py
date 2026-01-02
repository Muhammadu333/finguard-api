from fastapi import APIRouter, Depends

from app.db import get_cursor
from app.deps import get_current_user, require_role
from app.models import UserOut

router = APIRouter(tags=["users"])


@router.get("/me")
def me(user=Depends(get_current_user)):
    return {"user": user}


@router.get("/admin/users", response_model=list[UserOut])
def list_users(_admin=Depends(require_role({"admin"}))):
    with get_cursor() as cur:
        cur.execute("select id, email, role from users order by created_at desc limit 100")
        return cur.fetchall()

