from sqlmodel import Session, select
from datetime import datetime
from src.Models.subject import Subject
from src.schemas.subject import SubjectCreate, SubjectUpdate

class SubjectService:
    @staticmethod
    def create_subject(session: Session, subject_create: SubjectCreate, owner_id: int) -> Subject:
        db_subject = Subject(**subject_create.dict(), owner_id=owner_id)
        session.add(db_subject)
        session.commit()
        session.refresh(db_subject)
        return db_subject

    @staticmethod
    def get_subject(session: Session, subject_id: int) -> Subject | None:
        return session.get(Subject, subject_id)

    @staticmethod
    def get_subjects(session: Session, skip: int = 0, limit: int = 100) -> list[Subject]:
        statement = select(Subject).offset(skip).limit(limit)
        return session.exec(statement).all()

    @staticmethod
    def get_subjects_by_owner(session: Session, owner_id: int) -> list[Subject]:
        statement = select(Subject).where(Subject.owner_id == owner_id)
        return session.exec(statement).all()

    @staticmethod
    def update_subject(session: Session, subject: Subject, subject_update: SubjectUpdate) -> Subject:
        update_data = subject_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(subject, key, value)
        subject.updated_at = datetime.utcnow()
        session.add(subject)
        session.commit()
        session.refresh(subject)
        return subject

    @staticmethod
    def delete_subject(session: Session, subject_id: int) -> None:
        subject = session.get(Subject, subject_id)
        if not subject:
            raise ValueError("Subject not found")
        session.delete(subject)
        session.commit()