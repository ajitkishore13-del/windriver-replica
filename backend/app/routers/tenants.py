import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth import verify_basic_auth, get_tenant_header
from app.database import get_db
from app.models import Tenant
from app.schemas import TenantCreate, TenantResponse, PaginatedResponse

router = APIRouter(prefix="/tenants", tags=["Tenants"])


@router.get("", response_model=PaginatedResponse)
def list_tenants(
    _size: int = Query(1000),
    _offset: int = Query(0),
    _user=Depends(verify_basic_auth),
    db: Session = Depends(get_db),
):
    query = db.query(Tenant)
    total = query.count()
    items = query.offset(_offset).limit(_size).all()
    return {
        "items": [
            {
                "name": t.name,
                "created_at": t.created_at.isoformat() if t.created_at else None,
            }
            for t in items
        ],
        "metadata": {"pagination": {"total": total, "offset": _offset, "size": _size}},
    }


@router.post("", response_model=TenantResponse, status_code=201)
def create_tenant(
    body: TenantCreate,
    _user=Depends(verify_basic_auth),
    db: Session = Depends(get_db),
):
    existing = db.query(Tenant).filter(Tenant.name == body.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Tenant already exists")
    t = Tenant(name=body.name)
    db.add(t)
    db.commit()
    db.refresh(t)
    return {
        "name": t.name,
        "created_at": t.created_at.isoformat() if t.created_at else None,
    }


@router.delete("/{tenant_name}", status_code=204)
def delete_tenant(
    tenant_name: str,
    _user=Depends(verify_basic_auth),
    db: Session = Depends(get_db),
):
    t = db.query(Tenant).filter(Tenant.name == tenant_name).first()
    if not t:
        raise HTTPException(status_code=404, detail="Tenant not found")
    db.delete(t)
    db.commit()
