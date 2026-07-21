import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth import verify_basic_auth, get_tenant_header
from app.database import get_db
from app.models import Site
from app.schemas import SiteCreate, SiteResponse, PaginatedResponse

router = APIRouter(prefix="/sites", tags=["Sites"])


@router.get("", response_model=PaginatedResponse)
def list_sites(
    _size: int = Query(1000),
    _offset: int = Query(0),
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    query = db.query(Site).filter(Site.tenant_name == tenant)
    total = query.count()
    items = query.offset(_offset).limit(_size).all()
    return {
        "items": [
            {
                "name": s.name,
                "location": s.location or "",
                "tenant_name": s.tenant_name or "default_tenant",
                "created_at": s.created_at.isoformat() if s.created_at else None,
                "visibility": s.visibility or "tenant",
            }
            for s in items
        ],
        "metadata": {"pagination": {"total": total, "offset": _offset, "size": _size}},
    }


@router.get("/{site_name}", response_model=SiteResponse)
def get_site(
    site_name: str,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    s = db.query(Site).filter(
        Site.name == site_name, Site.tenant_name == tenant
    ).first()
    if not s:
        raise HTTPException(status_code=404, detail="Site not found")
    return {
        "name": s.name,
        "location": s.location or "",
        "tenant_name": s.tenant_name or "default_tenant",
        "created_at": s.created_at.isoformat() if s.created_at else None,
        "visibility": s.visibility or "tenant",
    }


@router.put("/{site_name}", response_model=SiteResponse)
def create_site(
    site_name: str,
    body: SiteCreate,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    existing = db.query(Site).filter(Site.name == site_name).first()
    if existing:
        existing.location = body.location or existing.location
        existing.visibility = body.visibility or existing.visibility
    else:
        s = Site(
            name=site_name,
            location=body.location or "",
            tenant_name=tenant,
            visibility=body.visibility or "tenant",
        )
        db.add(s)
        existing = s
    db.commit()
    db.refresh(existing)
    return {
        "name": existing.name,
        "location": existing.location or "",
        "tenant_name": existing.tenant_name or "default_tenant",
        "created_at": existing.created_at.isoformat() if existing.created_at else None,
        "visibility": existing.visibility or "tenant",
    }


@router.delete("/{site_name}", status_code=204)
def delete_site(
    site_name: str,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    s = db.query(Site).filter(
        Site.name == site_name, Site.tenant_name == tenant
    ).first()
    if not s:
        raise HTTPException(status_code=404, detail="Site not found")
    db.delete(s)
    db.commit()
