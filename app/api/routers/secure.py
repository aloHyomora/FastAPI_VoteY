from fastapi import APIRouter, Depends, Request
from app.api.dependencies import verify_api_key, verify_hmac

router = APIRouter(
    prefix="/secure",
    tags=["secure"],
    dependencies=[Depends(verify_api_key), Depends(verify_hmac)],
)

@router.get("/echo")
async def echo_get(request: Request):
    return {"ok": True}

@router.post("/echo")
async def echo_post(payload: dict, request: Request):
    return {"ok": True, "payload": payload}