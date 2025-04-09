from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/user")
def get_user(request: Request, username: str = "John"):
    return templates.TemplateResponse("index.html", {"request": request, "username": username})

@app.get("/greet")
def greeting(request: Request, time_of_day: str, username: str = "John"):
    return templates.TemplateResponse("greeting.html", {"request": request, "time_of_day": time_of_day, "username": username})

@app.get("/items")
def read_items(request: Request):
    my_items = ["apple", "banana", "cherry"]
    return templates.TemplateResponse("items.html", {"request": request, "items": my_items})

@app.get("/dynamic_items")
def read_dynamic_items(request: Request, item_list: str = ""):
    items = item_list.split(",")
    return templates.TemplateResponse("items.html", {"request": request, "items": items})

@app.get("/inherit")
def template_inherit(request: Request):
    my_text = "FastAPI와 Jinja2 템플릿 상속을 사용한 예제입니다."
    return templates.TemplateResponse("index.html", {"request": request, "text": my_text})