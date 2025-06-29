# database.py
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from passlib.hash import bcrypt

DATABASE_URL = "sqlite:///./csdata.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# 사용자 테이블 정의
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)  # 권한 필드 추가

# 상품 테이블 정의
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)          # 상품명
    price = Column(Integer)
    coupang_link = Column(String(2083))                 # 쿠팡 상품 페이지 URL
    taobao_link = Column(String(2083))                  # 타오바오 상품 페이지 URL
    coupang_options = Column(Text)                      # 쿠팡 옵션 목록 (이름과 가격 JSON 등으로 저장)
    taobao_options = Column(Text)                       # 타오바오 옵션 목록 (JSON 문자열 등)
    thumbnail = Column(String(2083))                    # 썸네일 이미지 URL
    details = Column(Text)                              # 제품 상세 정보 (예상 CS 답변 등)

__all__ = ["User", "Product", "SessionLocal", "Base"]

# ✅ 최초 관리자 계정 생성 (한 번만 실행되도록)
def create_super_admin():
    db = SessionLocal()
    if db.query(User).count() == 0:
        super_admin = User(
            username="shsboss274",  # 원하는 아이디
            password=bcrypt.hash("shsboss274"),  # 원하는 비밀로
            is_admin=True
        )
        db.add(super_admin)
        db.commit()
        print("✅ 최초 관리자 계정이 생성되었습니다. (shsboss274 / shsboss274)")
    db.close()

# DB 테이블 생성 및 최초 관리자 등록
Base.metadata.create_all(bind=engine)
create_super_admin()
