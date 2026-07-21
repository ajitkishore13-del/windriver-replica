from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth import verify_basic_auth, get_tenant_header
from app.database import get_db
from app.models import Event
from app.schemas import PaginatedResponse

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("", response_model=PaginatedResponse)
def list_events(
    execution_id: Optional[str] = Query(None),
    deployment_id: Optional[str] = Query(None),
    blueprint_id: Optional[str] = Query(None),
    level: Optional[str] = Query(None),
    _size: int = Query(1000),
    _offset: int = Query(0),
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    query = db.query(Event).filter(Event.tenant_name == tenant)
    if execution_id:
        query = query.filter(Event.execution_id == execution_id)
    if deployment_id:
        query = query.filter(Event.deployment_id == deployment_id)
    if level:
        query = query.filter(Event.level == level)
    total = query.count()
    items = query.order_by(Event.timestamp.desc()).offset(_offset).limit(_size).all()
    return {
        "items": [
            {
                "id": e.id,
                "timestamp": e.timestamp.isoformat() if e.timestamp else None,
                "message": e.message or "",
                "level": e.level or "info",
                "event_type": e.event_type or "workflow_succeeded",
                "execution_id": e.execution_id,
                "deployment_id": e.deployment_id,
                "blueprint_id": e.blueprint_id,
            }
            for e in items
        ],
        "metadata": {"pagination": {"total": total, "offset": _offset, "size": _size}},
    }
