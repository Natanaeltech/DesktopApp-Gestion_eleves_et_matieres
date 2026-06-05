from typing import Optional
from sqlmodel import Field
from sqlalchemy import String
from src.Models.base import Base

class User(Base, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_type=String(50))
    email: str = Field(sa_type=String(100), unique=True)
    password: str = Field(sa_type=String(100))
