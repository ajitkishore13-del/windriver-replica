import datetime
import hashlib
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth import verify_basic_auth, get_tenant_header
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserUpdate, UserResponse, PaginatedResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=PaginatedResponse)
def list_users(
    _size: int = Query(1000),
    _offset: int = Query(0),
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    query = db.query(User)
    total = query.count()
    items = query.offset(_offset).limit(_size).all()
    return {
        "items": [
            {
                "username": u.username,
                "role": u.role or "user",
                "tenant_name": u.tenant_name or "default_tenant",
                "created_at": u.created_at.isoformat() if u.created_at else None,
                "groups": u.groups or [],
            }
            for u in items
        ],
        "metadata": {"pagination": {"total": total, "offset": _offset, "size": _size}},
    }


@router.get("/{username}", response_model=UserResponse)
def get_user(
    username: str,
    _user=Depends(verify_basic_auth),
    db: Session = Depends(get_db),
):
    u = db.query(User).filter(User.username == username).first()
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "username": u.username,
        "role": u.role or "user",
        "tenant_name": u.tenant_name or "default_tenant",
        "created_at": u.created_at.isoformat() if u.created_at else None,
        "groups": u.groups or [],
    }


@router.post("", response_model=UserResponse, status_code=201)
def create_user(
    body: UserCreate,
    _user=Depends(verify_basic_auth),
    db: Session = Depends(get_db),
):
    existing = db.query(User).filter(User.username == body.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    pw_hash = hashlib.sha256(body.password.encode()).hexdigest()
    u = User(
        username=body.username,
        password=pw_hash,
        role=body.role or "user",
        tenant_name=body.tenant_name or "default_tenant",
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    return {
        "username": u.username,
        "role": u.role or "user",
        "tenant_name": u.tenant_name or "default_tenant",
        "created_at": u.created_at.isoformat() if u.created_at else None,
        "groups": u.groups or [],
    }


@router.patch("/{username}", response_model=UserResponse)
def update_user(
    username: str,
    body: UserUpdate,
    _user=Depends(verify_basic_auth),
    db: Session = Depends(get_db),
):
    u = db.query(User).filter(User.username == username).first()
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    if body.role is not None:
        u.role = body.role
    if body.password is not None:
        u.password = hashlib.sha256(body.password.encode()).hexdigest()
    db.commit()
    db.refresh(u)
    return {
        "username": u.username,
        "role": u.role or "user",
        "tenant_name": u.tenant_name or "default_tenant",
        "created_at": u.created_at.isoformat() if u.created_at else None,
        "groups": u.groups or [],
    }


@router.delete("/{username}", status_code=204)
def delete_user(
    username: str,
    _user=Depends(verify_basic_auth),
    db: Session = Depends(get_db),
):
    u = db.query(User).filter(User.username == username).first()
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(u)
    db.commit()
