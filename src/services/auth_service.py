from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlmodel import Session, select
from config import settings
from src.Models.token_blacklist import TokenBlacklist

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

class AuthService:
    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)

    @staticmethod
    def hash_password(plain: str) -> str:
        return pwd_context.hash(plain)

    @staticmethod
    def create_access_token(user_id: int) -> str:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {"sub": str(user_id), "exp": expire}
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    @staticmethod
    def decode_token(token: str):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload
        except JWTError:
            return None

    @staticmethod
    def is_token_blacklisted(token: str, session: Session) -> bool:
        statement = select(TokenBlacklist).where(TokenBlacklist.token == token)
        return session.exec(statement).first() is not None

    @staticmethod
    def blacklist_token(token: str, session: Session) -> None:
        blacklisted = TokenBlacklist(token=token)
        session.add(blacklisted)
        session.commit()
