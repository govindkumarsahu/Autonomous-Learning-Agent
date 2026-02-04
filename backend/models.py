from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserInDB(BaseModel):
    email: EmailStr
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class ProgressRecord(BaseModel):
    user_id: str
    topic: str
    attempt_number: int
    score: int
    date: datetime
