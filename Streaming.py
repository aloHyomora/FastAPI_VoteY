from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

def data_generator():
    for i in range(10000):
        yield f"data chunk {i}\n"

# FastAPI 경로 연산에 Streming Response 반환
@app.get("/stream")
def stream_data():
    generator = data_generator()
    return StreamingResponse(generator, media_type="text/plain")