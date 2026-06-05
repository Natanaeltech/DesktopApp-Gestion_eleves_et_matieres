from sqlmodel import Session, select
from datetime import datetime
from src.Models.etudiant import Etudiant
from src.schemas.etudiant import EtudiantCreate, EtudiantUpdate

class EtudiantService:
    @staticmethod
    def create_etudiant(session: Session, etudiant_create: EtudiantCreate, owner_id: int) -> Etudiant:
        db_etudiant = Etudiant(**etudiant_create.dict(), owner_id=owner_id)
        session.add(db_etudiant)
        session.commit()
        session.refresh(db_etudiant)
        return db_etudiant

    @staticmethod
    def get_etudiant(session: Session, etudiant_id: int) -> Etudiant | None:
        return session.get(Etudiant, etudiant_id)

    @staticmethod
    def get_etudiants(session: Session, skip: int = 0, limit: int = 100) -> list[Etudiant]:
        statement = select(Etudiant).offset(skip).limit(limit)
        return session.exec(statement).all()

    @staticmethod
    def get_etudiants_by_owner(session: Session, owner_id: int) -> list[Etudiant]:
        statement = select(Etudiant).where(Etudiant.owner_id == owner_id)
        return session.exec(statement).all()

    @staticmethod
    def update_etudiant(session: Session, etudiant: Etudiant, etudiant_update: EtudiantUpdate) -> Etudiant:
        update_data = etudiant_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(etudiant, key, value)
        etudiant.updated_at = datetime.utcnow()
        session.add(etudiant)
        session.commit()
        session.refresh(etudiant)
        return etudiant

    @staticmethod
    def delete_etudiant(session: Session, etudiant_id: int) -> None:
        etudiant = session.get(Etudiant, etudiant_id)
        if not etudiant:
            raise ValueError("Etudiant not found")
        session.delete(etudiant)
        session.commit()