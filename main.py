from fastapi import FastAPI
from pydantic import BaseModel, Field # Pydantic 라이브러리에서 BaseModel과 Field를 import합니다.
from typing import Optional, List

app = FastAPI() # Fast API 인스턴스를 생성합니다.

class Item(BaseModel): # Pydantic 모델을 정의합니다.
    # 'name' 필드는 필수이며, 최소 2자에서 최대 50자까지의 문자열입니다.
    name: str = Field(..., title="Item Name", min_length=2, max_length=50)

    # 'description' 필드는 선택적이며, 최대 300자까지의 문자열입니다.
    description: Optional[str] = Field(None, description="The description of the item", max_length=300)

    # 'price' 필드는 필수이며, 0보다 큰 실수입니다.
    price: float = Field(..., gt=0, description="The price must be greater than zero")

    # tag 필드는 선택적이며, 기본값으로 빈 리스트를 갖습니다. Json에서 'item-tags'라는 이름으로 매핑됩니다.
    tag: List[str] = Field(default=[], alias="item-tags")

@app.post("/items/")
def create_item(item: Item):
    return {"item": item.model_dump()}  # v2