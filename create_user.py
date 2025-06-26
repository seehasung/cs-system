from database import SessionLocal
from models import User
from passlib.hash import bcrypt

db = SessionLocal()

username = "admin"
password = "1234"

hashed_pw = bcrypt.hash(password)

user = User(username=username, password=hashed_pw)

db.add(user)
db.commit()

print(f"✅ 사용자 생성 완료: ID={username}, PW={password}")
