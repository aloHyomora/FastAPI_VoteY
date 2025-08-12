from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

app = FastAPI()

# 데이터베이스 연결 문자열을 설정합니다. 
# 여기서 사용자 이름, 비밀번호, 서버 주소, 데이터베이스 이름을 자신의 환경에 맞게 변경해야 합니다.
DATABASE_URL = "mysql+pymysql://root:Skinova0326!@localhost/fastdb"

# SQLAlchemy 엔진을 생성합니다. 이 엔진은 DB와의 모든 통신을 관리합니다.
engine = create_engine(DATABASE_URL)

# SQLAlchemy의 declarative_base() 함수를 호출하여 기본 클래스를 생성합니다.
# 이 클래스는 모든 모델 클래스의 상위 클래스로 사용됩니다.
Base = declarative_base()

class User(Base):
    # SQLAlchemy 모델을 위한 테이블 이름을 '__tablename__' 속성으로 설정합니다.
    __tablename__ = "users"

    # DB 테이블의 컬럼을 정의합니다. 여기선 'id', 'username', 'email' 컬럼을 정의합니다.
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(120))

# DB 엔진을 사용하여 DB에 테이블을 생성합니다.
# 이 코드는 서버 시작 시 DB에 'users' 테이블이 없으면 새로 생성합니다.
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}
