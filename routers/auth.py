# routers/auth.py

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from passlib.hash import bcrypt

from database import SessionLocal, User

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# 회원가입 페이지 보여주기
@router.get("/register", response_class=HTMLResponse)
def show_register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# 회원가입 처리
@router.post("/register")
def register_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    db: Session = SessionLocal()

    # 이미 존재하는 유저 확인
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "이미 존재하는 사용자입니다."
        })

    # 비밀번호 해시 후 저장
    hashed_pw = bcrypt.hash(password)
    new_user = User(username=username, password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.close()

    return RedirectResponse("/login", status_code=302)
