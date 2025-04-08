from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()  # Fast API 인스턴스를 생성합니다.

class Item(BaseModel):
    name: str
    price: float

# FastAPI 경로 연산을 정의합니다. 이 연산은 GET 요청을 처리합니다.
# 'response_model' 매개변수를 사용하여 Item을 지정하여 반환할 데이터의 구조를 정의합니다.
@app.get("/items/", response_model=Item)
def get_item():
    return {"name": "Sample Item", "price": 10.99}

