from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.config import settings
from app.api.routers import health, items

app = FastAPI(title=settings.APP_NAME)

# 기존 폴더 재사용
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# API 라우터 등록
app.include_router(health.router, prefix=settings.API_PREFIX)
app.include_router(items.router, prefix=settings.API_PREFIX)