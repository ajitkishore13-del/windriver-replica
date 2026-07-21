import secrets

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import verify_basic_auth
from app.database import get_db
from app.models import Token

router = APIRouter(prefix="/tokens", tags=["Tokens"])


@router.get("")
def get_tokens(_user=Depends(verify_basic_auth), db: Session = Depends(get_db)):
    token_value = secrets.token_urlsafe(32)
    full_token = "WyIwIiwiM" + secrets.token_urlsafe(16)
    db_token = Token(
        value=full_token,
        role=_user.role,
        username=_user.username,
    )
    db.add(db_token)
    db.commit()
    return {"role": _user.role, "value": full_token}
