from fastapi import FastAPI, APIRouter

app = FastAPI()
router = APIRouter()

@router.get("/items/")
def read_items():
    return {"message": "This is an item."}

@router.get("/users/")
def read_users():
    return {"message": "This is a user."}

app.include_router(router, prefix="/api/v1", tags=["items"])