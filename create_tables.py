from database import engine
from src.Models.base import Base
from src.Models.user import User
from src.Models.token_blacklist import TokenBlacklist
from src.Models.subject import Subject
from src.Models.etudiant import Etudiant

print("Création des tables...")
Base.metadata.create_all(bind=engine)
print("Tables créées avec succès.")
