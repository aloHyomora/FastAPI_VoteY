from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()  # Fast API 인스턴스를 생성합니다.

class Cat(BaseModel):
    name: str

class Dog(BaseModel):
    name: str

# 경로 연산을 정의합니다. 여기서 response_model은 Union[Cat, Dog]입니다.
@app.get("/animal/", response_model=Union[Cat, Dog])
def get_animal(animal: str):
    # 쿼리 매개변수로 전달된 'animal'에 따라 Cat 또는 Dog 객체를 반환합니다.
    if animal == "cat":
        return Cat(name="Whiskers")
    elif animal == "dog":
        return Dog(name="Fido")
    else:
        return {"error": "Invalid animal type. Use 'cat' or 'dog'."}
