from pydantic import BaseModel

class UserCreate(BaseModel):
    username:str
    password:str

class TokenResponse(BaseModel):
    sid: str
    api_token: str

class Userlogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    sid: str
    api_token: str

class Bookings(BaseModel):
    id: int
    type: str
    details: str