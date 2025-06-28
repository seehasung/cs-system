from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from database import Base, engine, SessionLocal, User
from routers import auth, admin

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="서하성")

templates = Jinja2Templates(directory="templates")

# DB 초기화
Base.metadata.create_all(bind=engine)

# 라우터 등록
app.include_router(auth.router)         # 로그인 등
app.include_router(admin.router)        # 관리자 관련


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    username = request.session.get("user")
    is_admin = False
    if username:
        db = SessionLocal()
        user = db.query(User).filter(User.username == username).first()
        db.close()
        if user:
            is_admin = user.is_admin

    return templates.TemplateResponse("index.html", {
        "request": request,
        "username": username,
        "is_admin": is_admin
    })
