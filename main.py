from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from database import Base, engine, SessionLocal, User
from routers import auth, admin

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="서하성")

templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)


# ✅ auth 라우터 등록
app.include_router(auth.router)
app.include_router(admin.router, prefix="/admin")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    username = request.session.get("user")  # ✅ 세션에서 사용자명 가져오기
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
