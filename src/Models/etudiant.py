from typing import Optional
from sqlmodel import Field
from datetime import datetime
from enum import Enum
from src.Models.base import Base

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

class Etudiant(Base, table=True):
    __tablename__ = "etudiant"
    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    age: int
    sexe: SexeEnum
    filiere: FiliereEnum
    grade: GradeEnum
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    owner_id: int = Field(foreign_key="user.id")
