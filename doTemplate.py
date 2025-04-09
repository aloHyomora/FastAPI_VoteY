from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, select_autoescape, FileSystemLoader

app = FastAPI()

env = Environment(
    loader=FileSystemLoader("templates"),  # 템플릿 파일이 있는 디렉토리
    autoescape=select_autoescape(['html']),
    extensions=['jinja2.ext.do']
)

templates = Jinja2Templates(directory="templates")  # 템플릿 디렉토리 설정
templates.env = env  # Jinja2 템플릿 환경 설정

@app.get("/do_example")
def do_example(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
