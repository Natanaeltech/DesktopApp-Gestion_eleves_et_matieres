from src.dependencies.auth import get_current_user
from src.Models.user import User
from sqlmodel import Session

_current_token: str | None = None

def set_token(token: str):
    global _current_token
    _current_token = token

def get_current_user_from_token(session: Session) -> User | None:
    if _current_token is None:
        return None
    try:
        return get_current_user(_current_token, session)
    except Exception:
        return None
