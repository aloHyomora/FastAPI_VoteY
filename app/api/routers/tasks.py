from __future__ import annotations
import asyncio
import uuid
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
import httpx

from app.api.dependencies import verify_api_key, verify_hmac
from app.services.http_client import get_http_client, request_with_retry

router = APIRouter(
    prefix="/secure/tasks",
    tags=["tasks"],
    dependencies=[Depends(verify_api_key), Depends(verify_hmac)],
)

async def do_work(payload: dict) -> dict:
    # 실제 로직으로 교체
    await asyncio.sleep(0.1)
    return {"echo": payload, "processed": True}

@router.post("/process")
async def process_sync(payload: dict):
    result = await do_work(payload)
    return {"status": "ok", "result": result}

@router.post("/process-async", status_code=202)
async def process_async(payload: dict, bg: BackgroundTasks, client: httpx.AsyncClient = Depends(get_http_client)):
    job_id = str(uuid.uuid4())

    async def _notify():
        try:
            result = await do_work(payload)
            body = {"job_id": job_id, "status": "ok", "result": result}
            # Spring 콜백 상대경로 예시: "callbacks/result" (=> OUTBOUND_BASE_URL + /callbacks/result)
            resp = await request_with_retry(client, "POST", "callbacks/result", json=body)
            resp.raise_for_status()
        except Exception as e:
            # 실패 시 재전송 전략/로그 적재 등 필요하면 확장
            pass

    # BackgroundTasks는 sync 함수만 지원 → 래핑
    def _runner():
        asyncio.run(_notify())

    bg.add_task(_runner)
    return {"accepted": True, "job_id": job_id}