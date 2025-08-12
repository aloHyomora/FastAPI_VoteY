from fastapi import Depends, FastAPI, APIRouter, HTTPException
from fastapi.routing import APIRoute

app = FastAPI()

def check_token(token: str):
    if token != "my-secret-token":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return token

router = APIRouter(dependencies=[Depends(check_token)])

@router.get("/items/")
def get_items():
    return {"message": "Access granted, you can view the items."}

@app.get("/public/")
def read_public():
    return {"message": "This is a public endpoint."}

app.include_router(router, prefix="/api/v1")