import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth import verify_basic_auth, get_tenant_header
from app.database import get_db
from app.models import Plugin
from app.schemas import PluginCreate, PluginResponse, PaginatedResponse

router = APIRouter(prefix="/plugins", tags=["Plugins"])


@router.get("", response_model=PaginatedResponse)
def list_plugins(
    _size: int = Query(1000),
    _offset: int = Query(0),
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    query = db.query(Plugin).filter(Plugin.tenant_name == tenant)
    total = query.count()
    items = query.offset(_offset).limit(_size).all()
    return {
        "items": [_p_to_dict(p) for p in items],
        "metadata": {"pagination": {"total": total, "offset": _offset, "size": _size}},
    }


@router.get("/{plugin_id}", response_model=PluginResponse)
def get_plugin(
    plugin_id: str,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    p = db.query(Plugin).filter(
        Plugin.id == plugin_id, Plugin.tenant_name == tenant
    ).first()
    if not p:
        raise HTTPException(status_code=404, detail="Plugin not found")
    return _p_to_dict(p)


@router.put("/{plugin_id}", response_model=PluginResponse)
def upload_plugin(
    plugin_id: str,
    body: PluginCreate,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    existing = db.query(Plugin).filter(Plugin.id == plugin_id).first()
    if existing:
        for k, v in body.dict(exclude_unset=True).items():
            setattr(existing, k, v)
    else:
        p = Plugin(
            id=plugin_id,
            package_name=body.package_name,
            package_version=body.package_version or "1.0.0",
            supported_platform=body.supported_platform or "linux",
            created_by=_user.username,
            tenant_name=tenant,
            visibility=body.visibility or "tenant",
        )
        db.add(p)
        existing = p
    db.commit()
    db.refresh(existing)
    return _p_to_dict(existing)


@router.delete("/{plugin_id}", status_code=204)
def delete_plugin(
    plugin_id: str,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    p = db.query(Plugin).filter(
        Plugin.id == plugin_id, Plugin.tenant_name == tenant
    ).first()
    if not p:
        raise HTTPException(status_code=404, detail="Plugin not found")
    db.delete(p)
    db.commit()


def _p_to_dict(p: Plugin):
    return {
        "id": p.id,
        "package_name": p.package_name or "",
        "package_version": p.package_version or "1.0.0",
        "supported_platform": p.supported_platform or "linux",
        "distribution": p.distribution or "centos",
        "distribution_release": p.distribution_release or "core",
        "uploaded_at": p.uploaded_at.isoformat() if p.uploaded_at else None,
        "created_by": p.created_by or "admin",
        "tenant_name": p.tenant_name or "default_tenant",
        "visibility": p.visibility or "tenant",
    }
