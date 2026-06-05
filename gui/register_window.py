import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, QPushButton,
                             QLabel, QMessageBox, QHBoxLayout)
from PyQt6.QtCore import Qt
from database import get_session
from src.services.user_service import UserService
from src.schemas.user import UserCreate
from src.services.auth_service import AuthService
from src.desktop_session import set_token
from gui.styles import apply_stylesheet   # <-- import ajouté

class RegisterWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Inscription - Créer un compte")
        self.setFixedSize(400, 350)
        self.setModal(True)
        apply_stylesheet(self)   # <-- application du même style que login

        layout = QVBoxLayout()
        layout.setSpacing(10)

        title = QLabel(" Créer un compte")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(title)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nom complet")
        self.name_input.setClearButtonEnabled(True)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.setClearButtonEnabled(True)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setClearButtonEnabled(True)
        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Confirmer le mot de passe")
        self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_input.setClearButtonEnabled(True)

        layout.addWidget(QLabel("Nom :"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Email :"))
        layout.addWidget(self.email_input)
        layout.addWidget(QLabel("Mot de passe :"))
        layout.addWidget(self.password_input)
        layout.addWidget(QLabel("Confirmation :"))
        layout.addWidget(self.confirm_input)

        btn_layout = QHBoxLayout()
        self.register_btn = QPushButton("S'inscrire")
        self.register_btn.clicked.connect(self.register)
        self.cancel_btn = QPushButton("Annuler")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.register_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def register(self):
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text()
        confirm = self.confirm_input.text()

        if not name or not email or not password:
            QMessageBox.warning(self, "Erreur", "Tous les champs sont obligatoires.")
            return

        if password != confirm:
            QMessageBox.warning(self, "Erreur", "Les mots de passe ne correspondent pas.")
            return

        try:
            with next(get_session()) as session:
                user_create = UserCreate(name=name, email=email, password=password)
                user = UserService.create_user(session, user_create)
                # Option : connecter automatiquement après inscription
                token = AuthService.create_access_token(user.id)
                set_token(token)
                QMessageBox.information(self, "Succès", "Compte créé avec succès !")
                self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Erreur", str(e))
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur inattendue : {e}")