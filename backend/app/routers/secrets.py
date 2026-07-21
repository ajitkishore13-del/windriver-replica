import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth import verify_basic_auth, get_tenant_header
from app.database import get_db
from app.models import Secret
from app.schemas import SecretCreate, SecretUpdate, SecretResponse, PaginatedResponse

router = APIRouter(prefix="/secrets", tags=["Secrets"])


@router.get("", response_model=PaginatedResponse)
def list_secrets(
    _size: int = Query(1000),
    _offset: int = Query(0),
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    query = db.query(Secret).filter(Secret.tenant_name == tenant)
    total = query.count()
    items = query.offset(_offset).limit(_size).all()
    return {
        "items": [_s_to_dict(s) for s in items],
        "metadata": {"pagination": {"total": total, "offset": _offset, "size": _size}},
    }


@router.get("/{key}", response_model=SecretResponse)
def get_secret(
    key: str,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    s = db.query(Secret).filter(
        Secret.key == key, Secret.tenant_name == tenant
    ).first()
    if not s:
        raise HTTPException(status_code=404, detail="Secret not found")
    return _s_to_dict(s)


@router.put("/{key}", response_model=SecretResponse)
def create_secret(
    key: str,
    body: SecretCreate,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    existing = db.query(Secret).filter(Secret.key == key).first()
    if existing:
        existing.value = body.value
        existing.hidden = body.hidden or False
        existing.visibility = body.visibility or "tenant"
        existing.updated_at = datetime.datetime.utcnow()
    else:
        s = Secret(
            key=key,
            value=body.value,
            hidden=body.hidden or False,
            tenant_name=tenant,
            created_by=_user.username,
            visibility=body.visibility or "tenant",
        )
        db.add(s)
        existing = s
    db.commit()
    db.refresh(existing)
    return _s_to_dict(existing)


@router.patch("/{key}", response_model=SecretResponse)
def update_secret(
    key: str,
    body: SecretUpdate,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    s = db.query(Secret).filter(
        Secret.key == key, Secret.tenant_name == tenant
    ).first()
    if not s:
        raise HTTPException(status_code=404, detail="Secret not found")
    if body.value is not None:
        s.value = body.value
    if body.visibility is not None:
        s.visibility = body.visibility
    if body.hidden is not None:
        s.hidden = body.hidden
    s.updated_at = datetime.datetime.utcnow()
    db.commit()
    db.refresh(s)
    return _s_to_dict(s)


@router.delete("/{key}", status_code=204)
def delete_secret(
    key: str,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    s = db.query(Secret).filter(
        Secret.key == key, Secret.tenant_name == tenant
    ).first()
    if not s:
        raise HTTPException(status_code=404, detail="Secret not found")
    db.delete(s)
    db.commit()


def _s_to_dict(s: Secret):
    return {
        "key": s.key,
        "hidden": s.hidden or False,
        "tenant_name": s.tenant_name or "default_tenant",
        "created_at": s.created_at.isoformat() if s.created_at else None,
        "updated_at": s.updated_at.isoformat() if s.updated_at else None,
        "created_by": s.created_by or "admin",
        "visibility": s.visibility or "tenant",
    }
