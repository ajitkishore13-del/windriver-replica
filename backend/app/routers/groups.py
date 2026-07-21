import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth import verify_basic_auth, get_tenant_header
from app.database import get_db
from app.models import Group
from app.schemas import GroupCreate, GroupUpdate, GroupResponse, PaginatedResponse

router = APIRouter(prefix="/groups", tags=["Groups"])


@router.get("", response_model=PaginatedResponse)
def list_groups(
    _size: int = Query(1000),
    _offset: int = Query(0),
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    query = db.query(Group).filter(Group.tenant_name == tenant)
    total = query.count()
    items = query.offset(_offset).limit(_size).all()
    return {
        "items": [
            {
                "name": g.name,
                "role": g.role or "user",
                "tenant_name": g.tenant_name or "default_tenant",
                "ldap_group": g.ldap_group or False,
                "created_at": g.created_at.isoformat() if g.created_at else None,
                "users": g.users or [],
            }
            for g in items
        ],
        "metadata": {"pagination": {"total": total, "offset": _offset, "size": _size}},
    }


@router.get("/{group_name}", response_model=GroupResponse)
def get_group(
    group_name: str,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    g = db.query(Group).filter(
        Group.name == group_name, Group.tenant_name == tenant
    ).first()
    if not g:
        raise HTTPException(status_code=404, detail="Group not found")
    return {
        "name": g.name,
        "role": g.role or "user",
        "tenant_name": g.tenant_name or "default_tenant",
        "ldap_group": g.ldap_group or False,
        "created_at": g.created_at.isoformat() if g.created_at else None,
        "users": g.users or [],
    }


@router.post("", response_model=GroupResponse, status_code=201)
def create_group(
    body: GroupCreate,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    existing = db.query(Group).filter(Group.name == body.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Group already exists")
    g = Group(
        name=body.name,
        role=body.role or "user",
        tenant_name=body.tenant_name or tenant,
    )
    db.add(g)
    db.commit()
    db.refresh(g)
    return {
        "name": g.name,
        "role": g.role or "user",
        "tenant_name": g.tenant_name or "default_tenant",
        "ldap_group": g.ldap_group or False,
        "created_at": g.created_at.isoformat() if g.created_at else None,
        "users": g.users or [],
    }


@router.patch("/{group_name}", response_model=GroupResponse)
def update_group(
    group_name: str,
    body: GroupUpdate,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    g = db.query(Group).filter(
        Group.name == group_name, Group.tenant_name == tenant
    ).first()
    if not g:
        raise HTTPException(status_code=404, detail="Group not found")
    if body.role is not None:
        g.role = body.role
    if body.users is not None:
        g.users = body.users
    db.commit()
    db.refresh(g)
    return {
        "name": g.name,
        "role": g.role or "user",
        "tenant_name": g.tenant_name or "default_tenant",
        "ldap_group": g.ldap_group or False,
        "created_at": g.created_at.isoformat() if g.created_at else None,
        "users": g.users or [],
    }


@router.delete("/{group_name}", status_code=204)
def delete_group(
    group_name: str,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    g = db.query(Group).filter(
        Group.name == group_name, Group.tenant_name == tenant
    ).first()
    if not g:
        raise HTTPException(status_code=404, detail="Group not found")
    db.delete(g)
    db.commit()
