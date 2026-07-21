from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth import verify_basic_auth, get_tenant_header
from app.database import get_db
from app.models import Agent
from app.schemas import AgentResponse, PaginatedResponse

router = APIRouter(prefix="/agents", tags=["Agents"])


@router.get("", response_model=PaginatedResponse)
def list_agents(
    deployment_id: Optional[str] = Query(None),
    node_ids: Optional[list[str]] = Query(None),
    node_instance_ids: Optional[list[str]] = Query(None),
    install_method: Optional[list[str]] = Query(None),
    _size: int = Query(1000),
    _offset: int = Query(0),
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    query = db.query(Agent).filter(Agent.tenant_name == tenant)
    if deployment_id:
        query = query.filter(Agent.deployment == deployment_id)
    total = query.count()
    items = query.offset(_offset).limit(_size).all()
    return {
        "items": [
            {
                "id": a.id,
                "host_id": a.host_id or a.id,
                "ip": a.ip or "127.0.0.1",
                "install_method": a.install_method or "remote",
                "system": a.system or "centos core",
                "version": a.version or "4.5.0",
                "node": a.node or "",
                "deployment": a.deployment,
            }
            for a in items
        ],
        "metadata": {"pagination": {"total": total, "offset": _offset, "size": _size}},
    }
