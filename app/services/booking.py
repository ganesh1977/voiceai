#from database import insert_booking
#from app.schemas import schemas
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
from app import models, schemas, crud, auth

def handle_booking(command: str,bookings: schemas.Bookings, db: Session = Depends(auth.get_db)):
    # Mock logic: extract keywords (you can integrate NLP)
    db_user = crud.bookngs(db, bookings)
    #insert_booking("booking", command)
    return {"message": "Booking confirmed", "details": command}
