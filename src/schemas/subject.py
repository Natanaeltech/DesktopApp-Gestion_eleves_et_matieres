from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class SubjectBase(BaseModel):
    nom: str
    matiere: str
    coefficient: int = Field(gt=0)

class SubjectCreate(SubjectBase):
    pass

class SubjectUpdate(BaseModel):
    nom: Optional[str] = None
    matiere: Optional[str] = None
    coefficient: Optional[int] = Field(None, gt=0)

class SubjectRead(SubjectBase):
    id: int
    created_at: datetime
    updated_at: datetime
    owner_id: int
    class Config:
        from_attributes = True
