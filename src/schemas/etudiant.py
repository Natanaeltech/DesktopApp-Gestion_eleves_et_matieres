from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class SexeEnum(str, Enum):
    M = "M"
    F = "F"

class FiliereEnum(str, Enum):
    DSI = "DSI"
    RMI = "RMI"

class GradeEnum(str, Enum):
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"
    M1 = "M1"
    M2 = "M2"

class EtudiantBase(BaseModel):
    nom: str
    age: int = Field(ge=0, le=120)
    sexe: SexeEnum
    filiere: FiliereEnum
    grade: GradeEnum

class EtudiantCreate(EtudiantBase):
    pass

class EtudiantUpdate(BaseModel):
    nom: Optional[str] = None
    age: Optional[int] = Field(None, ge=0, le=120)
    sexe: Optional[SexeEnum] = None
    filiere: Optional[FiliereEnum] = None
    grade: Optional[GradeEnum] = None

class EtudiantRead(EtudiantBase):
    id: int
    created_at: datetime
    updated_at: datetime
    owner_id: int
    class Config:
        from_attributes = True
