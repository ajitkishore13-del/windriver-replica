import datetime
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth import verify_basic_auth, get_tenant_header
from app.database import get_db
from app.models import Snapshot
from app.schemas import SnapshotResponse, PaginatedResponse

router = APIRouter(prefix="/snapshots", tags=["Snapshots"])


@router.get("", response_model=PaginatedResponse)
def list_snapshots(
    _size: int = Query(1000),
    _offset: int = Query(0),
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    query = db.query(Snapshot).filter(Snapshot.tenant_name == tenant)
    total = query.count()
    items = query.order_by(Snapshot.created_at.desc()).offset(_offset).limit(_size).all()
    return {
        "items": [
            {
                "id": s.id,
                "created_at": s.created_at.isoformat() if s.created_at else None,
                "status": s.status or "created",
                "created_by": s.created_by or "admin",
            }
            for s in items
        ],
        "metadata": {"pagination": {"total": total, "offset": _offset, "size": _size}},
    }


@router.post("", response_model=SnapshotResponse, status_code=201)
def create_snapshot(
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    snap_id = f"snap_{uuid.uuid4().hex[:8]}"
    s = Snapshot(
        id=snap_id,
        created_by=_user.username,
        tenant_name=tenant,
        status="created",
    )
    db.add(s)
    db.commit()
    db.refresh(s)
    return {
        "id": s.id,
        "created_at": s.created_at.isoformat() if s.created_at else None,
        "status": s.status or "created",
        "created_by": s.created_by or "admin",
    }


@router.delete("/{snapshot_id}", status_code=204)
def delete_snapshot(
    snapshot_id: str,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    s = db.query(Snapshot).filter(
        Snapshot.id == snapshot_id, Snapshot.tenant_name == tenant
    ).first()
    if not s:
        raise HTTPException(status_code=404, detail="Snapshot not found")
    db.delete(s)
    db.commit()
