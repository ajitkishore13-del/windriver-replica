from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import verify_basic_auth, get_tenant_header
from app.database import get_db
from app.models import Blueprint

router = APIRouter(prefix="/labels", tags=["Labels"])


@router.get("/blueprints")
def get_blueprint_label_keys(
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    blueprints = db.query(Blueprint).filter(Blueprint.tenant_name == tenant).all()
    keys = set()
    for b in blueprints:
        for label in (b.labels or []):
            if isinstance(label, dict):
                for k in label.keys():
                    keys.add(k)
    return {
        "items": list(keys),
        "metadata": {"pagination": {"total": len(keys), "offset": 0, "size": 1000}},
    }


@router.get("/blueprints/{label_key}")
def get_blueprint_label_values(
    label_key: str,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
    db: Session = Depends(get_db),
):
    blueprints = db.query(Blueprint).filter(Blueprint.tenant_name == tenant).all()
    values = set()
    for b in blueprints:
        for label in (b.labels or []):
            if isinstance(label, dict) and label_key in label:
                values.add(label[label_key])
    return {
        "items": list(values),
        "metadata": {"pagination": {"total": len(values), "offset": 0, "size": 1000}},
    }
