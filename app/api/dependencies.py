from fastapi import Header, HTTPException, status, Request
from app.core.config import settings
from app.utils.hmac_signer import verify_signature

def verify_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if x_api_key != settings.API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")

async def verify_hmac(
    request: Request,
    x_timestamp: str | None = Header(default=None),
    x_signature: str | None = Header(default=None),
) -> None:
    if not settings.HMAC_SECRET:
        raise HTTPException(status_code=500, detail="HMAC not configured")
    if not x_timestamp or not x_signature:
        raise HTTPException(status_code=401, detail="Missing HMAC headers")
    body = await request.body()
    ok = verify_signature(request.method, request.url.path, body, x_timestamp, x_signature, settings.HMAC_SECRET)
    if not ok:
        raise HTTPException(status_code=401, detail="Invalid HMAC signature")