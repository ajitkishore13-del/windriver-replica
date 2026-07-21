import datetime
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth import verify_basic_auth, get_tenant_header
from app.database import get_db
from app.models import Execution
from app.schemas import ExecutionStart, ExecutionAction, ExecutionResponse, PaginatedResponse

router = APIRouter(prefix="/executions", tags=["Executions"])


@router.get("", response_model=PaginatedResponse)
def list_executions(
    _include: Optional[str] = Query(None),
    deployment_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    _sort: Optional[list[str]] = Query(None),
    _size: int = Query(1000),
    _offset: int = Query(0),
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    query = db.query(Execution).filter(Execution.tenant_name == tenant)
    if deployment_id:
        query = query.filter(Execution.deployment_id == deployment_id)
    if status:
        query = query.filter(Execution.status == status)
    total = query.count()
    items = query.order_by(Execution.created_at.desc()).offset(_offset).limit(_size).all()
    return {
        "items": [_e_to_dict(e, _include) for e in items],
        "metadata": {"pagination": {"total": total, "offset": _offset, "size": _size}},
    }


@router.get("/{execution_id}", response_model=ExecutionResponse)
def get_execution(
    execution_id: str,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    e = db.query(Execution).filter(
        Execution.id == execution_id, Execution.tenant_name == tenant
    ).first()
    if not e:
        raise HTTPException(status_code=404, detail="Execution not found")
    return _e_to_dict(e)


@router.post("", response_model=ExecutionResponse, status_code=201)
def start_execution(
    body: ExecutionStart,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    exec_id = f"exec_{uuid.uuid4().hex[:8]}"
    e = Execution(
        id=exec_id,
        deployment_id=body.deployment_id,
        workflow_id=body.workflow_id,
        status="started",
        started_at=datetime.datetime.utcnow(),
        parameters=body.parameters or {},
        created_by=_user.username,
        tenant_name=tenant,
        execution_token=uuid.uuid4().hex,
    )
    db.add(e)
    db.commit()
    db.refresh(e)
    return _e_to_dict(e)


@router.post("/{execution_id}", response_model=ExecutionResponse)
def action_execution(
    execution_id: str,
    body: ExecutionAction,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    e = db.query(Execution).filter(
        Execution.id == execution_id, Execution.tenant_name == tenant
    ).first()
    if not e:
        raise HTTPException(status_code=404, detail="Execution not found")

    if body.action == "cancel":
        e.status = "cancelled"
    elif body.action == "force-cancel":
        e.status = "cancelled"
    elif body.action == "kill":
        e.status = "cancelled"
    elif body.action == "resume":
        e.status = "started"
        e.ended_at = None
        e.execution_token = uuid.uuid4().hex
    elif body.action == "force-resume":
        e.status = "started"
        e.ended_at = None
        e.execution_token = uuid.uuid4().hex
    else:
        raise HTTPException(status_code=400, detail=f"Unknown action: {body.action}")

    if body.action in ("cancel", "force-cancel", "kill"):
        e.ended_at = datetime.datetime.utcnow()

    db.commit()
    db.refresh(e)
    return _e_to_dict(e)


def _e_to_dict(e: Execution, _include: Optional[str] = None):
    result = {
        "id": e.id,
        "deployment_id": e.deployment_id,
        "blueprint_id": e.blueprint_id or "",
        "workflow_id": e.workflow_id,
        "status": e.status,
        "created_at": e.created_at.isoformat() if e.created_at else None,
        "started_at": e.started_at.isoformat() if e.started_at else None,
        "ended_at": e.ended_at.isoformat() if e.ended_at else None,
        "error": e.error,
        "created_by": e.created_by or "admin",
        "tenant_name": e.tenant_name or "default_tenant",
        "parameters": e.parameters or {},
        "is_system_workflow": e.is_system_workflow or False,
    }
    if _include:
        included = _include.split(",")
        return {k: v for k, v in result.items() if k in included}
    return result
