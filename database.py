# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Boolean
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

__all__ = ["User", "SessionLocal", "Base"]

# ✅ 최초 관리자 계정 생성 (한 번만 실행되도록)
def create_super_admin():
    db = SessionLocal()
    if db.query(User).count() == 0:
        super_admin = User(
            username="shsboss274",  # 원하는 아이디
            password=bcrypt.hash("shsboss274"),  # 원하는 비밀번호
            is_admin=True
        )
        db.add(super_admin)
        db.commit()
        print("✅ 최초 관리자 계정이 생성되었습니다. (shsboss274 / shsboss274)")
    db.close()

# DB 테이블 생성 및 최초 관리자 등록
Base.metadata.create_all(bind=engine)
create_super_admin()
