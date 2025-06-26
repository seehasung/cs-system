from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware  # ✅ 추가
from routers import auth
from database import Base, engine

app = FastAPI()

# ✅ 세션 미들웨어 추가 (비밀 키는 적절히 보안 필요)
app.add_middleware(SessionMiddleware, secret_key="서하성")

# 템플릿 경로
templates = Jinja2Templates(directory="templates")

# DB 생성
Base.metadata.create_all(bind=engine)

# 라우터 등록
app.include_router(auth.router)

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    username = request.cookies.get("username")  # 쿠키에서 사용자 이름 가져오기
    return templates.TemplateResponse("index.html", {"request": request, "username": username})

