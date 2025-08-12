from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse, PlainTextResponse, RedirectResponse

app = FastAPI()

# JsonResponse를 response_class로 사용하여 경로 연산을 정의합니다.
# 이 경로 연산은 Json 형식의 응답을 반환합니다.
@app.get("/json", response_class=JSONResponse)
def read_json():
    return {"message": "This is a JSON response"}

# HTMLResponse를 response_class로 사용하여 경로 연산을 정의합니다.
# 이 경로 연산은 HTML 형식의 응답을 반환합니다.
@app.get("/html", response_class=HTMLResponse)
def read_html():
    return "<html><body><h1>This is an HTML response</h1></body></html>"

# PlainTextResponse를 response_class로 사용하여 경로 연산을 정의합니다.
# 이 경로 연산은 일반 텍스트 형식의 응답을 반환합니다.
@app.get("/text", response_class=PlainTextResponse)
def read_text():
    return "This is a plain text response"

# RedirectResponse를 response_class로 사용하여 경로 연산을 정의합니다.
# 이 경로 연산은 다른 URL로 리디렉션하는 응답을 반환합니다.
@app.get("/redirect", response_class=RedirectResponse)
def read_redirect():
    return RedirectResponse(url="/json")