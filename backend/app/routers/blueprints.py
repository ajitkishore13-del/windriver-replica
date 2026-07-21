import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.auth import verify_basic_auth, get_tenant_header
from app.database import get_db
from app.models import Blueprint
from app.schemas import (
    BlueprintCreate, BlueprintResponse, BlueprintUpdate,
    PaginatedResponse, PaginationMetadata,
)

router = APIRouter(prefix="/blueprints", tags=["Blueprints"])


@router.get("", response_model=PaginatedResponse)
def list_blueprints(
    _include: Optional[str] = Query(None),
    id: Optional[list[str]] = Query(None),
    _sort: Optional[list[str]] = Query(None),
    _size: int = Query(1000),
    _offset: int = Query(0),
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    query = db.query(Blueprint).filter(Blueprint.tenant_name == tenant)
    if id:
        query = query.filter(Blueprint.id.in_(id))
    total = query.count()
    items = query.offset(_offset).limit(_size).all()
    return {
        "items": [_b_to_dict(b, _include) for b in items],
        "metadata": {"pagination": {"total": total, "offset": _offset, "size": _size}},
    }


@router.get("/{blueprint_id}", response_model=BlueprintResponse)
def get_blueprint(
    blueprint_id: str,
    _include: Optional[str] = Query(None),
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    b = db.query(Blueprint).filter(
        Blueprint.id == blueprint_id, Blueprint.tenant_name == tenant
    ).first()
    if not b:
        raise HTTPException(status_code=404, detail="Blueprint not found")
    return _b_to_dict(b, _include)


@router.put("/{blueprint_id}", response_model=BlueprintResponse)
def upload_blueprint(
    blueprint_id: str,
    body: BlueprintCreate,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    existing = db.query(Blueprint).filter(Blueprint.id == blueprint_id).first()
    if existing:
        for k, v in body.dict(exclude_unset=True).items():
            setattr(existing, k, v)
        existing.updated_at = datetime.datetime.utcnow()
    else:
        b = Blueprint(
            id=blueprint_id,
            description=body.description or "",
            main_file_name=body.application_file_name or "blueprint.yaml",
            plan=body.plan or {},
            created_by=_user.username,
            tenant_name=tenant,
            visibility=body.visibility or "tenant",
            labels=body.labels or [],
        )
        db.add(b)
        existing = b
    db.commit()
    db.refresh(existing)
    return _b_to_dict(existing)


@router.delete("/{blueprint_id}", status_code=204)
def delete_blueprint(
    blueprint_id: str,
    force: bool = Query(False),
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    b = db.query(Blueprint).filter(
        Blueprint.id == blueprint_id, Blueprint.tenant_name == tenant
    ).first()
    if not b:
        raise HTTPException(status_code=404, detail="Blueprint not found")
    db.delete(b)
    db.commit()


@router.get("/{blueprint_id}/archive")
def download_blueprint(
    blueprint_id: str,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    b = db.query(Blueprint).filter(
        Blueprint.id == blueprint_id, Blueprint.tenant_name == tenant
    ).first()
    if not b:
        raise HTTPException(status_code=404, detail="Blueprint not found")
    return {"message": "archive placeholder", "blueprint_id": blueprint_id}


@router.patch("/{blueprint_id}/set-visibility", response_model=BlueprintResponse)
def set_blueprint_visibility(
    blueprint_id: str,
    body: dict,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    b = db.query(Blueprint).filter(
        Blueprint.id == blueprint_id, Blueprint.tenant_name == tenant
    ).first()
    if not b:
        raise HTTPException(status_code=404, detail="Blueprint not found")
    b.visibility = body.get("visibility", "tenant")
    db.commit()
    db.refresh(b)
    return _b_to_dict(b)


@router.patch("/{blueprint_id}/set-global", response_model=BlueprintResponse)
def set_blueprint_global(
    blueprint_id: str,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    b = db.query(Blueprint).filter(
        Blueprint.id == blueprint_id, Blueprint.tenant_name == tenant
    ).first()
    if not b:
        raise HTTPException(status_code=404, detail="Blueprint not found")
    b.visibility = "global"
    db.commit()
    db.refresh(b)
    return _b_to_dict(b)


@router.patch("/{blueprint_id}", response_model=BlueprintResponse)
def update_blueprint_labels(
    blueprint_id: str,
    body: BlueprintUpdate,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    b = db.query(Blueprint).filter(
        Blueprint.id == blueprint_id, Blueprint.tenant_name == tenant
    ).first()
    if not b:
        raise HTTPException(status_code=404, detail="Blueprint not found")
    if body.labels is not None:
        b.labels = body.labels
    if body.description is not None:
        b.description = body.description
    b.updated_at = datetime.datetime.utcnow()
    db.commit()
    db.refresh(b)
    return _b_to_dict(b)


@router.patch("/{blueprint_id}/icon", response_model=BlueprintResponse)
def set_blueprint_icon(
    blueprint_id: str,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    b = db.query(Blueprint).filter(
        Blueprint.id == blueprint_id, Blueprint.tenant_name == tenant
    ).first()
    if not b:
        raise HTTPException(status_code=404, detail="Blueprint not found")
    db.commit()
    db.refresh(b)
    return _b_to_dict(b)


@router.put("/{blueprint_id}/validate")
def validate_blueprint(
    blueprint_id: str,
    body: BlueprintCreate = None,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    return {
        "id": f"exec_{blueprint_id}_validate",
        "status": "started",
        "workflow_id": "upload_blueprint",
        "deployment_id": None,
        "blueprint_id": blueprint_id,
    }


def _b_to_dict(b: Blueprint, _include: Optional[str] = None):
    d = {
        "id": b.id,
        "description": b.description or "",
        "main_file_name": b.main_file_name or "blueprint.yaml",
        "plan": b.plan or {},
        "created_at": b.created_at.isoformat() if b.created_at else None,
        "updated_at": b.updated_at.isoformat() if b.updated_at else None,
        "created_by": b.created_by or "admin",
        "tenant_name": b.tenant_name or "default_tenant",
        "visibility": b.visibility or "tenant",
        "private_resource": b.private_resource or False,
        "labels": b.labels or [],
    }
    if _include:
        included = _include.split(",")
        return {k: v for k, v in d.items() if k in included}
    return d
