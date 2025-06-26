from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from starlette.status import HTTP_302_FOUND
from passlib.hash import bcrypt

from database import SessionLocal
from models import User
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if user and bcrypt.verify(password, user.password):
        response = RedirectResponse(url="/", status_code=HTTP_302_FOUND)
        response.set_cookie("user", user.username)
        return response
    return templates.TemplateResponse("login.html", {"request": request, "error": "로그인 실패"})
