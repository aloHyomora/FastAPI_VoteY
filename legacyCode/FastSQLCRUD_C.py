from typing import Optional
from FastSQLStart import DATABASE_URL
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

# DB 설정을 위한 문자열을 정의합니다.
engine = create_engine(DATABASE_URL)

# SQLAlchemy의 모델 기본 클래스를 선언합니다. 
# 이 클래스를 상속받아 데이터에서 테이블을 정의할 수 있습니다.
Base = declarative_base()

class User(Base):
    # 'users' 테이블을 정의합니다.
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(120))

# Pydantic 모델을 정의합니다. 
# 이 모델은 FastAPI에서 요청 본문을 검증하는 데 사용됩니다.
class UserCreate(BaseModel):
    username: str
    email: str

# DB 세션을 생성하고 관리하는 의존성 함수를 정의합니다.
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

# DB 엔진을 사용하여 모델을 기반으로 테이블을 생성합니다.
Base.metadata.create_all(bind=engine)

# FastAPI 인스턴스를 생성합니다.
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# curl -X POST "http://127.0.0.1:8000/users/" -H "Content-Type: application/json" -d "{\"username\":\"KING\",\"email\":\"King@example.com\"}"
# curl -X 'GET' "http://127.0.0.1:8000/users/2" -H "accept: application/json"
# curl -X PUT "http://127.0.0.1:8000/users/1" -H "Content-Type: application/json" -d "{\"username\":\"newName\",\"email\":\"NEW@example.com\"}"
# curl -X DELETE "http://127.0.0.1:8000/users/3"
# 사용자를 생성하는 POST API 엔드포인트를 추가합니다.
@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Pydantic 모델을 사용하여 전달받은 데이터의 유효성을 검증하고, 새 User 인스턴스를 생성합니다.
    new_user = User(username=user.username, email=user.email)
    db.add(new_user)  # DB 세션에 새 사용자를 추가합니다.
    db.commit() # DB에 변경 사항을 커밋합니다.
    db.refresh(new_user)

    return {"id": new_user.id, "username": new_user.username, "email": new_user.email}    

# 사용자를 조회하는 GET API 엔드포인트를 추가합니다.
@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    # 주어진 ID를 가진 사용자를 DB에서 조회합니다.

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        return {"error": "User not found"}
    return {"id": user.id, "username": user.username, "email": user.email}

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None

# Update API 엔드포인트를 추가합니다.
@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        return {"error": "User not found"}
    
    if user.username is not None:
        db_user.username = user.username
    if user.email is not None:
        db_user.email = user.email

    db.commit()
    db.refresh(db_user)
    return {"id": db_user.id, "username": db_user.username, "email": db_user.email}

# Delete API 엔드포인트를 추가합니다.
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        return {"error": "User not found"}
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}