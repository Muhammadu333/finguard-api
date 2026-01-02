from fastapi import APIRouter, Depends, HTTPException

from app.db import get_cursor
from app.deps import get_current_user
from app.models import TransactionCreateIn, TransactionOut

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("", response_model=TransactionOut)
def create_transaction(payload: TransactionCreateIn, user=Depends(get_current_user)):
    with get_cursor() as cur:
        try:
            cur.execute(
                """
                insert into transactions (user_id, amount_kobo, currency, reference)
                values (%s, %s, %s, %s)
                returning id, user_id, amount_kobo, currency, reference
                """,
                (user["sub"], payload.amount_kobo, payload.currency, payload.reference),
            )
            return cur.fetchone()
        except Exception:
            raise HTTPException(status_code=409, detail="reference_in_use")


@router.get("", response_model=list[TransactionOut])
def list_transactions(user=Depends(get_current_user)):
    with get_cursor() as cur:
        cur.execute(
            """
            select id, user_id, amount_kobo, currency, reference
            from transactions
            where user_id = %s
            order by created_at desc
            limit 100
            """,
            (user["sub"],),
        )
        return cur.fetchall()

