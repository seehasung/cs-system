from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Optional
import json

from database import SessionLocal, User, Product

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# ✅ 사용자 목록 보기 (검색 포함)
@router.get("/users", response_class=HTMLResponse)
def admin_users(request: Request, search: str = ""):
    username = request.session.get("user")
    if not username:
        return RedirectResponse("/login", status_code=302)

    db: Session = SessionLocal()
    current_user = db.query(User).filter(User.username == username).first()
    if not current_user or not current_user.is_admin:
        db.close()
        return RedirectResponse("/", status_code=302)

    users = db.query(User).filter(User.username.contains(search)).all() if search else db.query(User).all()
    db.close()
    return templates.TemplateResponse("admin_users_bootstrap.html", {
        "request": request,
        "users": users,
        "username": username,
        "search": search
    })

# ✅ 사용자 이름 수정
@router.post("/users/update")
def update_user(user_id: int = Form(...), new_username: str = Form(...)):
    db: Session = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.username = new_username
        db.commit()
    db.close()
    return RedirectResponse("/admin/users", status_code=302)

# ✅ 관리자 권한 토글
@router.post("/users/toggle-admin")
def toggle_admin(user_id: int = Form(...)):
    db: Session = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.is_admin = not user.is_admin
        db.commit()
    db.close()
    return RedirectResponse("/admin/users", status_code=302)

# ✅ 사용자 삭제
@router.post("/users/delete")
def delete_user(user_id: int = Form(...)):
    db: Session = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user and user.username != 'admin':
        db.delete(user)
        db.commit()
    db.close()
    return RedirectResponse("/admin/users", status_code=302)

# ✅ 상품 목록 보기
@router.get("/products", response_class=HTMLResponse)
def product_list(request: Request, keyword: str = ""):
    db = SessionLocal()
    products = db.query(Product).filter(Product.name.contains(keyword)).all() if keyword else db.query(Product).all()
    db.close()
    return templates.TemplateResponse("admin_products.html", {
        "request": request,
        "products": products,
        "keyword": keyword
    })

# ✅ 상품 등록 폼
@router.get("/products/create", response_class=HTMLResponse)
def product_create_form(request: Request):
    return templates.TemplateResponse("product_form.html", {
        "request": request,
        "product": None,
        "coupang_options": [],
        "taobao_options": []
    })
    
# ✅ 상품 등록 처리
@router.post("/products/create")
def product_create(
    request: Request,
    name: str = Form(...),
    price: int = Form(...),
    coupang_link: Optional[str] = Form(""),
    taobao_link: Optional[str] = Form(""),
    coupang_option_names: Optional[List[str]] = Form([]),
    coupang_option_prices: Optional[List[int]] = Form([]),
    taobao_option_names: Optional[List[str]] = Form([]),
    taobao_option_prices: Optional[List[int]] = Form([]),
    thumbnail: Optional[str] = Form(""),
    details: Optional[str] = Form("")
):
    coupang_options = json.dumps([
        {"name": n, "price": p} for n, p in zip(coupang_option_names, coupang_option_prices)
    ])
    taobao_options = json.dumps([
        {"name": n, "price": p} for n, p in zip(taobao_option_names, taobao_option_prices)
    ])

    db = SessionLocal()
    new_product = Product(
        name=name,
        price=price,
        coupang_link=coupang_link,
        taobao_link=taobao_link,
        coupang_options=coupang_options,
        taobao_options=taobao_options,
        thumbnail=thumbnail,
        details=details
    )
    db.add(new_product)
    db.commit()
    db.close()
    return RedirectResponse("/admin/products", status_code=302)

# ✅ 상품 상세 보기
@router.get("/products/{product_id}", response_class=HTMLResponse)
def product_detail(request: Request, product_id: int):
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == product_id).first()
    db.close()
    if not product:
        return RedirectResponse("/admin/products", status_code=302)
    return templates.TemplateResponse("product_detail.html", {
        "request": request,
        "product": product,
        "coupang_options": json.loads(product.coupang_options or "[]"),
        "taobao_options": json.loads(product.taobao_options or "[]")
    })





# ✅ 상품 수정 폼
@router.get("/products/edit/{product_id}", response_class=HTMLResponse)
def edit_product_form(request: Request, product_id: int):
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == product_id).first()
    db.close()
    return templates.TemplateResponse("product_form.html", {
        "request": request,
        "product": product,
        "coupang_options": json.loads(product.coupang_options or "[]"),
        "taobao_options": json.loads(product.taobao_options or "[]")
    })

# ✅ 상품 수정 처리
@router.post("/products/edit/{product_id}")
def edit_product(
    product_id: int,
    name: str = Form(...),
    price: int = Form(...),
    coupang_link: Optional[str] = Form(""),
    taobao_link: Optional[str] = Form(""),
    coupang_option_names: Optional[List[str]] = Form([]),
    coupang_option_prices: Optional[List[int]] = Form([]),
    taobao_option_names: Optional[List[str]] = Form([]),
    taobao_option_prices: Optional[List[int]] = Form([]),
    thumbnail: Optional[str] = Form(""),
    details: Optional[str] = Form("")
):
    coupang_options = json.dumps([
        {"name": n, "price": p} for n, p in zip(coupang_option_names, coupang_option_prices)
    ])
    taobao_options = json.dumps([
        {"name": n, "price": p} for n, p in zip(taobao_option_names, taobao_option_prices)
    ])

    db = SessionLocal()
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        product.name = name
        product.price = price
        product.coupang_link = coupang_link
        product.taobao_link = taobao_link
        product.coupang_options = coupang_options
        product.taobao_options = taobao_options
        product.thumbnail = thumbnail
        product.details = details
        db.commit()
    db.close()
    return RedirectResponse("/admin/products", status_code=302)

# ✅ 상품 삭제
@router.post("/products/delete")
def product_delete(product_id: int = Form(...)):
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
    db.close()
    return RedirectResponse("/admin/products", status_code=302)
