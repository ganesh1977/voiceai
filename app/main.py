from fastapi import FastAPI, Depends, HTTPException, Request, Form,BackgroundTasks
from . import models, schemas, crud, auth
import database
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
import httpx
from pydantic import BaseModel
from database import engine, SessionLocal
from app.speech_handler import process_speech_command
from app.spark_handler import init_spark
import logging
from fastapi.responses import PlainTextResponse

spark = init_spark()

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI() 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
load_dotenv()

EXOTEL_SID = os.getenv("EXOTEL_SID")
EXOTEL_TOKEN = os.getenv("EXOTEL_TOKEN")
EXOPHONE = os.getenv("EXOTEL_VIRTUAL_NUMBER")

BASE_URL = f"https://{EXOTEL_SID}:{EXOTEL_TOKEN}@api.exotel.com/v1/Accounts/{EXOTEL_SID}"

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

@app.post('/loginUser')
def loginUser(user: schemas.Userlogin,db: Session = Depends(auth.get_db)):
    print(models.User.username)
    db_user = db.query(models.User).filter(models.User.username == user.username).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    if not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    return db_user

@app.get("/userslist/{id}")
def usersList(db: Session = Depends(auth.get_db)):
    users = db.query(models.User).all()
    return users

class CallRequest(BaseModel):
    hospital_id: str
    phone_number: str

@app.post("/make-call")
async def make_call(call: CallRequest):
    print(call.hospital_id," - ",call.phone_number)
    hospital_id = call.hospital_id
    phone_number = call.phone_number
    """Trigger a call via Exotel tied to a hospital's ID."""
    async with httpx.AsyncClient() as client:
        data = {
            "From": phone_number,            # Verified user number
            "To": os.getenv("CALLER_NUMBER"),# Your team/hospital support
            "CallerId": EXOPHONE,
            "TimeLimit": "300",
            "TimeOut": "30",
            "StatusCallback": f"https://127.0.0.1:8000/call-status/{hospital_id}",
            "CustomField": f"hospital_id={hospital_id}"
        }
        print(data)

        response = await client.post(
            f"{BASE_URL}/Calls/connect.json",
            data=data
        )

        return {
            "status_code": response.status_code,
            "data": response.json()
        }

@app.post("/call-status/{hospital_id}")
async def call_status_callback(hospital_id: str, request: Request):
    form_data = await request.form()
    status = form_data.get("CallStatus")
    call_sid = form_data.get("CallSid")
    recording_url = form_data.get("RecordingUrl")
    # You could save this to a DB or notify staff
    print(f"Hospital: {hospital_id} | Status: {status} | Call SID: {call_sid} | Recording: {recording_url}")
    return {"message": "Callback received"}
    
@app.post("/voice-command/")
def handle_voice_command():
    bookings = schemas.Bookings
    db = Depends(auth.get_db)
    command_text = process_speech_command()
    print(f"SELECT '{command_text}' AS command")
    result = spark.sql(f"SELECT '{command_text}' AS command")
    print(result)
    command = result.collect()[0]['command']
        # Simple routing logic (in real-world, use NLP parser)
    if "book" in command.lower():
        from app.services.booking import handle_booking
        db_user = crud.create_user(db, bookings)
        return db_user
    elif "ticket" in command.lower():
        from app.services.ticket import handle_ticket
        return handle_ticket(command)
    elif "grocery" in command.lower():
        from app.services.grocery import handle_grocery
        return handle_grocery(command)
    else:
        return {"message": "Command not recognized"}

class WebhookRequest(BaseModel):
    hospital_id: str
    phone_number: str

logger = logging.getLogger("uvicorn")

@app.post("/webhook/exotel")
async def exotel_webhook(
    From: str = Form("From"),
    To: str = Form("To"),
    CallSid: str = Form("CallSid"),
    CallType: str = Form("CallType"),
    Direction: str = Form("Direction"),
    StartTime: str = Form("StartTime"),
    EndTime: str = Form("EndTime"),
    Status: str = Form("Status")
):
    print("ganesh ganesh ganesh")
    logger.info("Exotel Webhook received: From=%s, To=%s, CallSid=%s", From, To, CallSid)

    # Process the data as needed
    return PlainTextResponse("OK", status_code=200)

@app.post("/webhook")
async def receive_webhook(request: Request):
    print("abcdef")
    data = request.form()
    print(data)
    # Process your data here
    return {"message": "Webhook received!"}

# Background task function
def process_data(data):
    print("📦 Background task started")
    print(data)

@app.post("/async-webhook")
async def async_webhook(request: Request,background_tasks: BackgroundTasks):
    data = request.form()    
    # Offload processing to a background task
    background_tasks.add_task(process_data, data)
    return {"message": "Webhook received, processing in background"}

