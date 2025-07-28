from fastapi import Depends, HTTPException, Header
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal
from .crud import get_user_by_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_token(api_token: str = Header(...), db: Session = Depends(get_db)):
    user = get_user_by_token(db, api_token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API Token")
    return 

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
