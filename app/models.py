from sqlalchemy import Column,Integer, String, DateTime, func, ForeignKey
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(100))
    sid = Column(String(50), unique=True, index=True)
    api_token = Column(String(255), unique=True)
    created_at = Column(DateTime, default=func.now())

class Hospital(Base):
    __tablename__ = "Hospital"
    id = Column(Integer, primary_key=True, index=True)
    hospitalname = Column(String(50), unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    hospital_add = Column(String(255))    
    created_at = Column(DateTime, default=func.now())

class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True, autoincrement=True)  # ✅ REQUIRED
    type = Column(String(100))
    details = Column(String(100))  # or DateTime

class Ticket(Base):
    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True, autoincrement=True)  # ✅ REQUIRED
    type = Column(String(100))
    details = Column(String(100))  # or DateTime

class Call(Base):
    __tablename__ = "calls"

    id = Column(Integer, primary_key=True, index=True)
    call_sid = Column(String(100))
    call_from = Column(String(20))
    call_to = Column(String(20))
    call_type = Column(String(20))
    dial_whom_number = Column(String(20))
    start_time = Column(String(100))
    end_time = Column(String(100))
    status = Column(String(20))
    direction = Column(String(20))

class CallLog(Base):
    __tablename__ = "call_logs"

    id = Column(Integer, primary_key=True, index=True)
    call_sid = Column(String(64), unique=True, index=True)
    call_from = Column(String(20))
    call_to = Column(String(20))
    status = Column(String(20))
    duration = Column(String(10), nullable=True)
    recording_url = Column(String(255), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

class CallDetail(Base):
    __tablename__ = "call_details"

    id = Column(Integer, primary_key=True, index=True)
    call_sid = Column(String(100), unique=True, nullable=False)
    call_from = Column(String(20))
    call_to = Column(String(20))
    call_type = Column(String(50))
    call_status = Column(String(50))
    start_time = Column(String(100))
    end_time = Column(String(100))
    duration = Column(String(50))
    price = Column(String(50))
    recording_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)