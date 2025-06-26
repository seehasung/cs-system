from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers import auth
from database import Base, engine

app = FastAPI()

# 템플릿 경로
templates = Jinja2Templates(directory="templates")

# DB 생성
Base.metadata.create_all(bind=engine)

# 라우터 등록
app.include_router(auth.router)
