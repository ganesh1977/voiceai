from sqlalchemy import Column,Integer, String, DateTime, func, ForeignKey
from database import Base

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