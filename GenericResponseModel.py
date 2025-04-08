from fastapi import FastAPI
from pydantic.generics import GenericModel
from typing import TypeVar, Generic

app = FastAPI()  # Fast API 인스턴스를 생성합니다.

T = TypeVar("T")  # 제네릭 타입 변수를 정의합니다.

# GenericModel을 상속받아 제네릭 응답 모델을 정의합니다.
class GenericItem(GenericModel, Generic[T]):
    data: T

# 경로 연산에서 'response_model' 매개변수를 사용하여 제네릭 응답 모델을 지정합니다.
# 반환되는 'data' 필드가 문자열 타입임을 명시합니다.
@app.get("/generic_item/", response_model=GenericItem[str])
def get_generic_item():
    return {"data": "This is a generic item response."}
