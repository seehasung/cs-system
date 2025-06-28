from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal, User

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# ✅ 관리자 페이지
@router.get("/admin/logs", response_class=HTMLResponse)
def admin_page(request: Request):
    username = request.session.get("user")  # ✅ 세션으로 사용자 확인
    if not username:
        return RedirectResponse("/login", status_code=302)

    db: Session = SessionLocal()
    user = db.query(User).filter(User.username == username).first()

    if not user or not user.is_admin:
        db.close()
        return RedirectResponse("/", status_code=302)

    users = db.query(User).all()
    db.close()

    return templates.TemplateResponse("admin_users.html", {
        "request": request,
        "users": users
    })

# ✅ 사용자 이름 수정
@router.post("/admin/users/update")
def update_user(user_id: int = Form(...), new_username: str = Form(...)):
    db = SessionLocal()
    user = db.query(User).get(user_id)
    if user:
        user.username = new_username
        db.commit()
    db.close()
    return RedirectResponse("/admin", status_code=302)

# ✅ 관리자 권한 토글
@router.post("/admin/users/toggle-admin")
def toggle_admin(user_id: int = Form(...)):
    db = SessionLocal()
    user = db.query(User).get(user_id)
    if user and user.username != "shsboss274":
        user.is_admin = not user.is_admin
        db.commit()
    db.close()
    return RedirectResponse("/admin", status_code=302)

# ✅ 사용자 삭제
@router.post("/admin/users/delete")
def delete_user(user_id: int = Form(...)):
    db = SessionLocal()
    user = db.query(User).get(user_id)
    if user and user.username != "shsboss274":
        db.delete(user)
        db.commit()
    db.close()
    return RedirectResponse("/admin", status_code=302)
