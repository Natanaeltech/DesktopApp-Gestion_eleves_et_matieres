from sqlmodel import Session
from src.services.auth_service import AuthService
from src.services.user_service import UserService

def get_current_user(token: str, session: Session):
    if AuthService.is_token_blacklisted(token, session):
        raise PermissionError("Token revoked")
    payload = AuthService.decode_token(token)
    if not payload:
        raise ValueError("Invalid token")
    user_id = payload.get("sub")
    if not user_id:
        raise ValueError("Invalid token payload")
    user = UserService.get_by_id(session, int(user_id))
    if not user:
        raise ValueError("User not found")
    return user