from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message + "\n")

@app.get("/")
async def read_root(background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, "root endpoint was reached")
    return {"message": "Hello World"}