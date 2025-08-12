from fastapi import APIRouter, Depends
from app.schemas.item import Item
from app.api.dependencies import verify_api_key

router = APIRouter(prefix="/items", tags=["items"], dependencies=[Depends(verify_api_key)])

@router.post("/")
def create_item(item: Item):
    return {"item": item.model_dump()}