from sqlalchemy.orm import Session
from . import models, schemas, utils

def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = utils.hash_password(user.password)
    sid = utils.create_sid()
    token = utils.create_token({"sub": user.username})
    db_user = models.User(
        username=user.username,
        hashed_password=hashed_pw,
        sid=sid,
        api_token=token
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_token(db: Session, token: str):
    return db.query(models.User).filter(models.User.api_token == token).first()

def loginCheck(User: schemas.Userlogin, db: Session):
    return db.query(models.User)
