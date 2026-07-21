import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth import verify_basic_auth, get_tenant_header
from app.database import get_db
from app.models import Deployment
from app.schemas import (
    DeploymentCreate, DeploymentResponse, DeploymentUpdate,
    PaginatedResponse,
)

router = APIRouter(prefix="/deployments", tags=["Deployments"])


@router.get("", response_model=PaginatedResponse)
def list_deployments(
    _include: Optional[str] = Query(None),
    id: Optional[list[str]] = Query(None),
    blueprint_id: Optional[str] = Query(None),
    _sort: Optional[list[str]] = Query(None),
    _size: int = Query(1000),
    _offset: int = Query(0),
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    query = db.query(Deployment).filter(Deployment.tenant_name == tenant)
    if id:
        query = query.filter(Deployment.id.in_(id))
    if blueprint_id:
        query = query.filter(Deployment.blueprint_id == blueprint_id)
    total = query.count()
    items = query.offset(_offset).limit(_size).all()
    return {
        "items": [_d_to_dict(d, _include) for d in items],
        "metadata": {"pagination": {"total": total, "offset": _offset, "size": _size}},
    }


@router.get("/{deployment_id}", response_model=DeploymentResponse)
def get_deployment(
    deployment_id: str,
    _include: Optional[str] = Query(None),
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    d = db.query(Deployment).filter(
        Deployment.id == deployment_id, Deployment.tenant_name == tenant
    ).first()
    if not d:
        raise HTTPException(status_code=404, detail="Deployment not found")
    return _d_to_dict(d, _include)


@router.put("/{deployment_id}", response_model=DeploymentResponse)
def create_deployment(
    deployment_id: str,
    body: DeploymentCreate,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    existing = db.query(Deployment).filter(Deployment.id == deployment_id).first()
    if existing:
        for k, v in body.dict(exclude_unset=True).items():
            setattr(existing, k, v)
        existing.updated_at = datetime.datetime.utcnow()
    else:
        d = Deployment(
            id=deployment_id,
            display_name=body.display_name or deployment_id,
            blueprint_id=body.blueprint_id,
            inputs=body.inputs or {},
            outputs={},
            capabilities={},
            created_by=_user.username,
            tenant_name=tenant,
            visibility=body.visibility or "tenant",
            site_name=body.site_name,
            runtime_only_evaluation=body.runtime_only_evaluation or False,
            skip_plugins_validation=body.skip_plugins_validation or False,
            labels=body.labels or [],
            status="active",
        )
        db.add(d)
        existing = d
    db.commit()
    db.refresh(existing)
    return _d_to_dict(existing)


@router.delete("/{deployment_id}", status_code=204)
def delete_deployment(
    deployment_id: str,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    d = db.query(Deployment).filter(
        Deployment.id == deployment_id, Deployment.tenant_name == tenant
    ).first()
    if not d:
        raise HTTPException(status_code=404, detail="Deployment not found")
    db.delete(d)
    db.commit()


@router.patch("/{deployment_id}", response_model=DeploymentResponse)
def update_deployment(
    deployment_id: str,
    body: DeploymentUpdate,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    d = db.query(Deployment).filter(
        Deployment.id == deployment_id, Deployment.tenant_name == tenant
    ).first()
    if not d:
        raise HTTPException(status_code=404, detail="Deployment not found")
    if body.labels is not None:
        d.labels = body.labels
    if body.inputs is not None:
        d.inputs = body.inputs
    if body.visibility is not None:
        d.visibility = body.visibility
    d.updated_at = datetime.datetime.utcnow()
    db.commit()
    db.refresh(d)
    return _d_to_dict(d)


@router.get("/{deployment_id}/outputs")
def get_deployment_outputs(
    deployment_id: str,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    d = db.query(Deployment).filter(
        Deployment.id == deployment_id, Deployment.tenant_name == tenant
    ).first()
    if not d:
        raise HTTPException(status_code=404, detail="Deployment not found")
    return {"outputs": d.outputs or {}}


@router.get("/{deployment_id}/capabilities")
def get_deployment_capabilities(
    deployment_id: str,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    d = db.query(Deployment).filter(
        Deployment.id == deployment_id, Deployment.tenant_name == tenant
    ).first()
    if not d:
        raise HTTPException(status_code=404, detail="Deployment not found")
    return d.capabilities or {}


def _d_to_dict(d: Deployment, _include: Optional[str] = None):
    result = {
        "id": d.id,
        "display_name": d.display_name or d.id,
        "blueprint_id": d.blueprint_id,
        "created_at": d.created_at.isoformat() if d.created_at else None,
        "updated_at": d.updated_at.isoformat() if d.updated_at else None,
        "created_by": d.created_by or "admin",
        "tenant_name": d.tenant_name or "default_tenant",
        "visibility": d.visibility or "tenant",
        "private_resource": d.private_resource or False,
        "labels": d.labels or [],
        "inputs": d.inputs or {},
        "outputs": d.outputs or {},
        "capabilities": d.capabilities or {},
        "site_name": d.site_name,
        "runtime_only_evaluation": d.runtime_only_evaluation or False,
        "skip_plugins_validation": d.skip_plugins_validation or False,
        "status": d.status or "active",
    }
    if _include:
        included = _include.split(",")
        return {k: v for k, v in result.items() if k in included}
    return result
