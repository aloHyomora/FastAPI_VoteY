from FastSQLStart import DATABASE_URL
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

# FastAPI 애플리케이션 인스턴스를 생성하여 애플리케이션을 초기화합니다.
app = FastAPI()

# 데이터베이스 연결 설정
engine = create_engine(DATABASE_URL)


# SessionLocal 인스턴스를 생성하기 위한 factory를 정의합니다.
# autocommit과 autoflush를 False로 설정하여, 
# 데이터베이스 세션 관리를 더욱 세밀하게 제어할 수 있습니다.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy의 declarative_base() 함수를 호출하여 기본 클래스를 생성합니다.
Base = declarative_base()

# User 모델을 정의합니다.
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(120))

# Pydantic 모델을 정의합니다.
# 이 모델은 FastAPI에서 요청 본문을 검증하는 데 사용됩니다.
class UserCreate(BaseModel):
    username: str
    email: str

# SQLAlchemy 모델 기반으로 DB에 테이블을 생성합니다.
# 만약 테이블이 이미 존재한다면, 아무런 작업도 수행하지 않습니다.
Base.metadata.create_all(bind=engine)

# '/users/' 경로에 POST 요청을 받는 엔드포인트를 생성합니다.
# 이 함수는 새로운 사용자를 생성하고 데이터베이스에 저장하는 역할을 합니다.
@app.post("/users/")
def create_user(user: UserCreate):
    # SessionLocal()을 호출하여 DB 세션을 생성합니다.
    db = SessionLocal()
    # User 인스턴스를 생성하고 초기화합니다.
    new_user = User(username=user.username, email=user.email)
    # DB 세션에 새 사용자를 추가합니다.
    db.add(new_user)
    # DB에 변경 사항을 커밋합니다.
    db.commit()
    # DB에서 새 사용자 정보를 갱신합니다.
    db.refresh(new_user)
    # DB 세션을 종료합니다.
    db.close()
    # 새 사용자 정보를 JSON 형식으로 반환합니다.
    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email
    }