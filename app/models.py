from sqlalchemy import Column,Integer, String, DateTime , func
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(100))
    sid = Column(String(50), unique=True, index=True)
    api_token = Column(String(255), unique=True)
    created_at = Column(DateTime, default=func.now())
    