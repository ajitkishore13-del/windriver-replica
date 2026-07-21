from fastapi import APIRouter, Depends

from app.auth import verify_basic_auth

router = APIRouter(tags=["Status"])


@router.get("/status")
def get_status():
    return {"status": "running"}


@router.post("/login")
def login(user=Depends(verify_basic_auth)):
    return {
        "username": user.username,
        "role": user.role,
        "tenant_name": user.tenant_name,
        "token": f"WyIwIiwiM{user.username}",
    }
