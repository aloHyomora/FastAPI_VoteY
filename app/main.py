from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import httpx

from app.core.config import settings
from app.api.routers import health, items, remote, secure
from app.middleware.request_id import RequestIdMiddleware
from app.services.http_client import _add_headers_hook


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = httpx.AsyncClient(
        base_url=settings.OUTBOUND_BASE_URL,
        timeout=settings.REQUEST_TIMEOUT,
        event_hooks={"request": [_add_headers_hook]},
    )
    try:
        yield
    finally:
        await app.state.http_client.aclose()


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

# CORS(필요 시 도메인 제한)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 요청 ID
app.add_middleware(RequestIdMiddleware)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 라우터
app.include_router(health.router, prefix=settings.API_PREFIX)
app.include_router(items.router, prefix=settings.API_PREFIX)
app.include_router(remote.router, prefix=settings.API_PREFIX)
app.include_router(secure.router, prefix=settings.API_PREFIX)