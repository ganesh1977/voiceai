from fastapi import FastAPI, Depends
from . import models, schemas, crud, auth
import database 
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.post("/register", response_model=schemas.TokenResponse)
def register(user: schemas.UserCreate, db: Session = Depends(auth.get_db)):
    db_user = crud.create_user(db, user)
    return {
        "sid": db_user.sid,
        "api_token": db_user.api_token
    }

@app.get("/protected")
def protected(user=Depends(auth.verify_token)):
    return {"message": f"Hello {user.username}, this is a protected route!"}
