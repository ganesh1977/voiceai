from pydantic import BaseModel

class UserCreate(BaseModel):
    username:str
    password:str

class TokenResponse(BaseModel):
    sid: str
    api_token: str
