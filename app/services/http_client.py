from __future__ import annotations
import asyncio
import httpx
from fastapi import Request
from app.core.config import settings
from app.utils.hmac_signer import now_ts, sign

RETRYABLE_STATUS = {408, 429, 500, 502, 503, 504}

def get_http_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.http_client  # type: ignore[attr-defined]

async def _add_headers_hook(request: httpx.Request):
    # API Key
    if settings.OUTBOUND_API_KEY:
        request.headers.setdefault("X-API-Key", settings.OUTBOUND_API_KEY)
    # HMAC
    if settings.HMAC_SECRET:
        ts = now_ts()
        body = request.content or b""
        sig = sign(request.method, request.url.path, body, ts, settings.HMAC_SECRET)
        request.headers["X-Timestamp"] = ts
        request.headers["X-Signature"] = sig

async def request_with_retry(
    client: httpx.AsyncClient,
    method: str,
    url: str,
    *,
    json: dict | None = None,
    headers: dict | None = None,
    max_retries: int = 3,
    initial_backoff: float = 0.2,
) -> httpx.Response:
    backoff = initial_backoff
    for attempt in range(1, max_retries + 1):
        try:
            resp = await client.request(method, url, json=json, headers=headers)
            if resp.status_code in RETRYABLE_STATUS and attempt < max_retries:
                await asyncio.sleep(backoff)
                backoff *= 2
                continue
            return resp
        except (httpx.ConnectError, httpx.ReadTimeout):
            if attempt >= max_retries:
                raise
            await asyncio.sleep(backoff)
            backoff *= 2