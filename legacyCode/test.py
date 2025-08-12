from fastapi import FastAPI # FastAPI 라이브러리를 import합니다.

app = FastAPI() # Fast API 인스턴스를 생성합니다.

@app.get("/")  # HTTP GET 요청을  "/" 경로에 매핑합니다.
def read_root():  # 루트 경로에 대한 요청을 처리할 함수를 정의합니다.
    return {"message": "Hello, FastAPI!"} # JSON 형식으로 응답을 반환합니다.

@app.get("/items/{item_id}") # HTTP GET 요청을 "/items/{item_id}" 경로에 매핑합니다.
def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/getdata/")
def get_data(data: str = "default"):
    return {"data": data}

@app.get("/items/")
def read_items(skip = 0, limit = 10):
    return {"skip": skip, "limit": limit}

