from fastapi import FastAPI, APIRouter
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# TrustedHostMiddleware를 추가합니다.
# 이 미들웨어는 들어오는 모든 요청의 호스트가 allowed_hosts에 지정된 호스트 중 하나인지 검사합니다.
# 만약 요청이 허용되지 않은 호스트에서 온 것이라면, 404 Bad Request 에러를 반환합니다.
# 이는 서비스가 지정된 호스트(도메인)에서만 접근 가능하도록 보안을 강화하는 데 도움을 줍니다.


app = FastAPI()
router = APIRouter()
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["example.com", "localhost", "127.0.0.1"]
)

@router.get("/items/")
def read_items_from_router():
    return {"message": "You are accessing the API from an allowed host via router."}

@router.get("/users/")
def read_users():
    return {"message": "This is a user."}

app.include_router(router, prefix="/api/v1", tags=["items"])
