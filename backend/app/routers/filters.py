import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth import verify_basic_auth, get_tenant_header
from app.database import get_db
from app.models import Filter
from app.schemas import FilterCreate, FilterResponse, PaginatedResponse

router = APIRouter(prefix="/filters", tags=["Filters"])


@router.get("", response_model=PaginatedResponse)
def list_filters(
    _size: int = Query(1000),
    _offset: int = Query(0),
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    query = db.query(Filter).filter(Filter.tenant_name == tenant)
    total = query.count()
    items = query.offset(_offset).limit(_size).all()
    return {
        "items": [
            {
                "id": f.id,
                "blueprint_id": f.blueprint_id,
                "deployment_id": f.deployment_id,
                "execution_id": f.execution_id,
                "rules": f.rules or {},
                "created_at": f.created_at.isoformat() if f.created_at else None,
            }
            for f in items
        ],
        "metadata": {"pagination": {"total": total, "offset": _offset, "size": _size}},
    }


@router.post("", response_model=FilterResponse, status_code=201)
def create_filter(
    body: FilterCreate,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    f = Filter(
        id=body.id,
        blueprint_id=body.blueprint_id,
        deployment_id=body.deployment_id,
        execution_id=body.execution_id,
        rules=body.rules or {},
        tenant_name=tenant,
    )
    db.add(f)
    db.commit()
    db.refresh(f)
    return {
        "id": f.id,
        "blueprint_id": f.blueprint_id,
        "deployment_id": f.deployment_id,
        "execution_id": f.execution_id,
        "rules": f.rules or {},
        "created_at": f.created_at.isoformat() if f.created_at else None,
    }


@router.delete("/{filter_id}", status_code=204)
def delete_filter(
    filter_id: str,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    f = db.query(Filter).filter(
        Filter.id == filter_id, Filter.tenant_name == tenant
    ).first()
    if not f:
        raise HTTPException(status_code=404, detail="Filter not found")
    db.delete(f)
    db.commit()
