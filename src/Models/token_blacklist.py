from typing import Optional
from sqlmodel import Field
from datetime import datetime
from src.Models.base import Base

class TokenBlacklist(Base, table=True):
    __tablename__ = "token_blacklist"
    id: Optional[int] = Field(default=None, primary_key=True)
    token: str = Field(unique=True, index=True)
    blacklisted_at: datetime = Field(default_factory=datetime.utcnow)
