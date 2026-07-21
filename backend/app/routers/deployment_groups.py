import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth import verify_basic_auth, get_tenant_header
from app.database import get_db
from app.models import DeploymentGroup, Deployment
from app.schemas import (
    DeploymentGroupCreate, DeploymentGroupUpdate, DeploymentGroupResponse,
    PaginatedResponse,
)

router = APIRouter(prefix="/deployment-groups", tags=["Deployment Groups"])


@router.get("", response_model=PaginatedResponse)
def list_deployment_groups(
    _size: int = Query(1000),
    _offset: int = Query(0),
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    query = db.query(DeploymentGroup).filter(DeploymentGroup.tenant_name == tenant)
    total = query.count()
    items = query.offset(_offset).limit(_size).all()
    return {
        "items": [_g_to_dict(g) for g in items],
        "metadata": {"pagination": {"total": total, "offset": _offset, "size": _size}},
    }


@router.get("/{group_id}", response_model=DeploymentGroupResponse)
def get_deployment_group(
    group_id: str,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    g = db.query(DeploymentGroup).filter(
        DeploymentGroup.id == group_id, DeploymentGroup.tenant_name == tenant
    ).first()
    if not g:
        raise HTTPException(status_code=404, detail="Deployment group not found")
    return _g_to_dict(g)


@router.put("/{group_id}", response_model=DeploymentGroupResponse)
def create_deployment_group(
    group_id: str,
    body: DeploymentGroupCreate,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    existing = db.query(DeploymentGroup).filter(DeploymentGroup.id == group_id).first()
    if existing:
        for k, v in body.dict(exclude_unset=True).items():
            setattr(existing, k, v)
    else:
        g = DeploymentGroup(
            id=group_id,
            display_name=body.display_name or group_id,
            description=body.description or "",
            created_by=_user.username,
            tenant_name=tenant,
            visibility=body.visibility or "tenant",
            default_blueprint_id=body.default_blueprint_id,
            default_inputs=body.default_inputs or {},
            labels=body.labels or [],
        )
        db.add(g)
        existing = g
    db.commit()
    db.refresh(existing)
    return _g_to_dict(existing)


@router.patch("/{group_id}", response_model=DeploymentGroupResponse)
def update_deployment_group(
    group_id: str,
    body: DeploymentGroupUpdate,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    g = db.query(DeploymentGroup).filter(
        DeploymentGroup.id == group_id, DeploymentGroup.tenant_name == tenant
    ).first()
    if not g:
        raise HTTPException(status_code=404, detail="Deployment group not found")
    for k, v in body.dict(exclude_unset=True).items():
        setattr(g, k, v)
    db.commit()
    db.refresh(g)
    return _g_to_dict(g)


@router.delete("/{group_id}", status_code=204)
def delete_deployment_group(
    group_id: str,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    g = db.query(DeploymentGroup).filter(
        DeploymentGroup.id == group_id, DeploymentGroup.tenant_name == tenant
    ).first()
    if not g:
        raise HTTPException(status_code=404, detail="Deployment group not found")
    db.delete(g)
    db.commit()


@router.post("/{group_id}/add-deployments", response_model=DeploymentGroupResponse)
def add_deployments_to_group(
    group_id: str,
    body: dict,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    g = db.query(DeploymentGroup).filter(
        DeploymentGroup.id == group_id, DeploymentGroup.tenant_name == tenant
    ).first()
    if not g:
        raise HTTPException(status_code=404, detail="Deployment group not found")
    new_ids = body.get("deployment_ids", [])
    current = g.deployment_ids or []
    g.deployment_ids = list(set(current + new_ids))
    db.commit()
    db.refresh(g)
    return _g_to_dict(g)


@router.post("/{group_id}/remove-deployments", response_model=DeploymentGroupResponse)
def remove_deployments_from_group(
    group_id: str,
    body: dict,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    g = db.query(DeploymentGroup).filter(
        DeploymentGroup.id == group_id, DeploymentGroup.tenant_name == tenant
    ).first()
    if not g:
        raise HTTPException(status_code=404, detail="Deployment group not found")
    remove_ids = body.get("deployment_ids", [])
    current = g.deployment_ids or []
    g.deployment_ids = [did for did in current if did not in remove_ids]
    db.commit()
    db.refresh(g)
    return _g_to_dict(g)


def _g_to_dict(g: DeploymentGroup):
    return {
        "id": g.id,
        "display_name": g.display_name or g.id,
        "description": g.description or "",
        "created_at": g.created_at.isoformat() if g.created_at else None,
        "created_by": g.created_by or "admin",
        "tenant_name": g.tenant_name or "default_tenant",
        "visibility": g.visibility or "tenant",
        "private_resource": g.private_resource or False,
        "default_blueprint_id": g.default_blueprint_id,
        "default_inputs": g.default_inputs or {},
        "deployment_ids": g.deployment_ids or [],
        "labels": g.labels or [],
    }
