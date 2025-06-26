from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    return "<h1>✅ FastAPI CS 프로그램이 정상 작동합니다!</h1>"
