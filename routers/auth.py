from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from datetime import datetime
import os

from database import SessionLocal, User

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# ✅ 로그 기록 함수
def log_event(event: str):
    os.makedirs("logs", exist_ok=True)
    with open("logs/user_events.log", "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {event}\n")

# ✅ 회원가입 폼
@router.get("/register", response_class=HTMLResponse)
def show_register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# ✅ 회원가입 처리
@router.post("/register")
def register_user(request: Request, username: str = Form(...), password: str = Form(...)):
    db: Session = SessionLocal()

    if db.query(User).filter(User.username == username).first():
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "이미 존재하는 사용자입니다."
        })

    hashed_pw = bcrypt.hash(password)
    new_user = User(username=username, password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.close()

    log_event(f"✅ 회원가입: {username}")
    return RedirectResponse("/login", status_code=302)

# ✅ 로그인 폼
@router.get("/login", response_class=HTMLResponse)
def show_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# ✅ 로그인 처리 (세션 사용)
@router.post("/login")
def login_user(request: Request, username: str = Form(...), password: str = Form(...)):
    db: Session = SessionLocal()
    user = db.query(User).filter(User.username == username).first()

    if not user or not bcrypt.verify(password, user.password):
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "아이디 또는 비밀번호가 잘못되었습니다."
        })

    request.session["user"] = username  # ✅ 세션 저장
    log_event(f"✅ 로그인: {username}")
    return RedirectResponse("/", status_code=302)

# ✅ 로그아웃
@router.get("/logout")
def logout(request: Request):
    username = request.session.get("user")
    request.session.clear()  # ✅ 세션 초기화
    log_event(f"🔓 로그아웃: {username}")
    return RedirectResponse("/login", status_code=302)

# ✅ 비밀번호 변경 폼
@router.get("/change-password", response_class=HTMLResponse)
def show_change_password_form(request: Request):
    username = request.session.get("user")
    if not username:
        return RedirectResponse("/login", status_code=302)
    return templates.TemplateResponse("change_password.html", {"request": request})

# ✅ 비밀번호 변경 처리
@router.post("/change-password")
def change_password(request: Request, current_password: str = Form(...), new_password: str = Form(...)):
    username = request.session.get("user")
    if not username:
        return RedirectResponse("/login", status_code=302)

    db: Session = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    if not user or not bcrypt.verify(current_password, user.password):
        return templates.TemplateResponse("change_password.html", {
            "request": request,
            "error": "현재 비밀번호가 올바르지 않습니다."
        })

    user.password = bcrypt.hash(new_password)
    db.commit()
    db.close()

    log_event(f"🔑 비밀번호 변경: {username}")
    return RedirectResponse("/", status_code=302)
