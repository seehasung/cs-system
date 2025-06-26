from fastapi import FastAPI, Request  # ✅ Request 추가
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers import auth
from database import Base, engine
from fastapi.responses import HTMLResponse

app = FastAPI()

# 템플릿 경로 설정
templates = Jinja2Templates(directory="templates")

# DB 테이블 생성
Base.metadata.create_all(bind=engine)

# 라우터 등록
app.include_router(auth.router)

# 메인 페이지
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
