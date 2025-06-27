from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from database import Base, engine, SessionLocal, User

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="서하성")

templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    username = request.cookies.get("username")
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
