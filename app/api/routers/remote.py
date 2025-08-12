from fastapi import APIRouter, Depends, HTTPException
import httpx
from app.schemas.item import Item
from app.services.http_client import request_with_retry, get_http_client

router = APIRouter(prefix="/remote", tags=["remote"])

def _raise_for_status(resp: httpx.Response):
    try:
        resp.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"upstream error {resp.status_code}: {resp.text}") from e

@router.get("/health")
async def remote_health(client: httpx.AsyncClient = Depends(get_http_client)):
    try:
        # base_url이 .../api 이므로 상대경로 사용
        resp = await request_with_retry(client, "GET", "health")
        _raise_for_status(resp)
        return resp.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"remote health failed: {e}") from e

@router.post("/items")
async def remote_create_item(item: Item, client: httpx.AsyncClient = Depends(get_http_client)):
    try:
        resp = await request_with_retry(client, "POST", "items/", json=item.model_dump(by_alias=True))
        _raise_for_status(resp)
        return resp.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"remote create failed: {e}") from e

@router.get("/secure-echo")
async def remote_secure_echo(client: httpx.AsyncClient = Depends(get_http_client)):
    try:
        resp = await request_with_retry(client, "GET", "secure/echo")
        _raise_for_status(resp)
        return resp.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"remote secure echo failed: {e}") from e

@router.post("/secure-echo")
async def remote_secure_echo_post(payload: dict, client: httpx.AsyncClient = Depends(get_http_client)):
    try:
        resp = await request_with_retry(client, "POST", "secure/echo", json=payload)
        _raise_for_status(resp)
        return resp.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"remote secure echo failed: {e}") from e