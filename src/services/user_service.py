from sqlmodel import Session, select
from src.Models.user import User
from src.schemas.user import UserCreate, UserUpdate
from src.services.auth_service import AuthService

class UserService:
    @staticmethod
    def get_by_email(session: Session, email: str) -> User | None:
        return session.exec(select(User).where(User.email == email)).first()

    @staticmethod
    def get_by_id(session: Session, user_id: int) -> User | None:
        return session.get(User, user_id)

    @staticmethod
    def create_user(session: Session, user_create: UserCreate) -> User:
        if UserService.get_by_email(session, user_create.email):
            raise ValueError("Email already exists")   # au lieu de HTTPException
        hashed = AuthService.hash_password(user_create.password)
        db_user = User(name=user_create.name, email=user_create.email, password=hashed)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

    @staticmethod
    def update_user(session: Session, user: User, user_update: UserUpdate) -> User:
        update_data = user_update.dict(exclude_unset=True)
        if "password" in update_data:
            update_data["password"] = AuthService.hash_password(update_data["password"])
        for key, value in update_data.items():
            setattr(user, key, value)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user