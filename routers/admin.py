# routers/admin.py

from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal, User

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 관리자 확인
def is_admin_user(request: Request):
    username = request.cookies.get("username")
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    return user and user.is_admin

# 사용자 목록 보기
@router.get("/admin/users", response_class=HTMLResponse)
def manage_users(request: Request, db: Session = Depends(get_db)):
    if not is_admin_user(request):
        return RedirectResponse(url="/", status_code=302)

    users = db.query(User).all()
    return templates.TemplateResponse("admin_users.html", {"request": request, "users": users})

# 사용자 삭제
@router.post("/admin/users/delete")
def delete_user(user_id: int = Form(...), request: Request = None, db: Session = Depends(get_db)):
    if not is_admin_user(request):
        return RedirectResponse(url="/", status_code=302)

    user = db.query(User).filter(User.id == user_id).first()
    if user and user.username != "admin":
        db.delete(user)
        db.commit()
    return RedirectResponse("/admin/users", status_code=302)

# 권한 토글
@router.post("/admin/users/toggle-admin")
def toggle_admin(user_id: int = Form(...), request: Request = None, db: Session = Depends(get_db)):
    if not is_admin_user(request):
        return RedirectResponse(url="/", status_code=302)

    user = db.query(User).filter(User.id == user_id).first()
    if user and user.username != "admin":
        user.is_admin = not user.is_admin
        db.commit()
    return RedirectResponse("/admin/users", status_code=302)

# 사용자 정보 변경
@router.post("/admin/users/update")
def update_user(
    user_id: int = Form(...),
    new_username: str = Form(...),
    request: Request = None,
    db: Session = Depends(get_db)
):
    if not is_admin_user(request):
        return RedirectResponse(url="/", status_code=302)

    user = db.query(User).filter(User.id == user_id).first()
    if user and user.username != "admin":
        user.username = new_username
        db.commit()
    return RedirectResponse("/admin/users", status_code=302)
