import json
from pathlib import Path
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api.dependencies import verify_api_key  # 추가

router = APIRouter(
    prefix="/issue-total",
    tags=["issue-total"],
    dependencies=[Depends(verify_api_key)],  # API Key 보안 적용
)

# 간단 캐시
_cache: dict | None = None
_file_path = Path(settings.DATA_DIR) / "summary_results_final.json"

def _load():
    global _cache
    if _cache is not None:
        return _cache
    if not _file_path.is_file():
        raise HTTPException(status_code=404, detail="data file not found")
    try:
        with _file_path.open("r", encoding="utf-8") as f:
            _cache = json.load(f)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="invalid json format")
    return _cache

@router.get("", summary="summary_results_final.json 전체 반환")
async def get_all():
    data = _load()
    return JSONResponse(content=data, media_type="application/json; charset=utf-8")

@router.post("/refresh", summary="캐시 리프레시(데이터 파일 변경 후 호출)")
async def refresh():
    global _cache
    _cache = None
    data = _load()
    return {"refreshed": True, "has_issue_total": "issue_total" in data}