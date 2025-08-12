from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()  # Fast API 인스턴스를 생성합니다.

class Item(BaseModel):
    name: str

# 경로 연산을 정의합니다. 여기서 response_model은 List[Item]입니다.
@app.get("/items/", response_model=List[Item])
def get_items():
    # 여러 개의 Item 객체를 반환합니다.
    return [
        {"name": "Item 1"},
        {"name": "Item 2"},
        {"name": "Item 3"}
    ]