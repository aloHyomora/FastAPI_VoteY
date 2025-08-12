from fastapi import FastAPI, Depends, HTTPException, APIRouter

app = FastAPI()

# 공통 의존성 함수
def common_dependency():
    return "Common Dependency"

# 상위 라우터
parent_router = APIRouter(
    prefix="/parent",
    tags=["parent"],
    dependencies=[Depends(common_dependency)]
)

@parent_router.get("/item")
def get_parent_item():
    return {"message": "This is a parent item."}

# 하위 라우터
child_router = APIRouter()

@child_router.get("/item")
def get_child_item(common: str = Depends(common_dependency)):    
    return {"message": "This is a child item.",  "common": common}

# 하위 라우터를 상위 라우터에 추가 (상속)
parent_router.include_router(child_router, prefix="/child")

# 상위 라우터를 애플리케이션에 추가
app.include_router(parent_router)


