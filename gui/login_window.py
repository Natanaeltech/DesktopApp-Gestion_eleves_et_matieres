import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, QPushButton,
                             QLabel, QMessageBox, QHBoxLayout)
from PyQt6.QtCore import Qt
from database import get_session
from src.services.user_service import UserService
from src.services.auth_service import AuthService
from src.desktop_session import set_token
from gui.register_window import RegisterWindow
from gui.styles import apply_stylesheet

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connexion - Gestion des matières et étudiants")
        self.setFixedSize(400, 300)
        apply_stylesheet(self)

        layout = QVBoxLayout()
        layout.setSpacing(10)

        title = QLabel(" Authentification")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(title)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.setClearButtonEnabled(True)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setClearButtonEnabled(True)

        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)
        layout.addWidget(QLabel("Mot de passe:"))
        layout.addWidget(self.password_input)

        btn_layout = QHBoxLayout()
        self.login_btn = QPushButton("Se connecter")
        self.login_btn.clicked.connect(self.login)
        self.register_btn = QPushButton("S'inscrire")
        self.register_btn.clicked.connect(self.open_register)
        btn_layout.addWidget(self.login_btn)
        btn_layout.addWidget(self.register_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        if not email or not password:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs")
            return

        with next(get_session()) as session:
            user = UserService.get_by_email(session, email)
            if not user or not AuthService.verify_password(password, user.password):
                QMessageBox.warning(self, "Erreur", "Email ou mot de passe incorrect")
                return
            token = AuthService.create_access_token(user.id)
            set_token(token)
            self.accept()

    def open_register(self):
        # Cacher la fenêtre de login pendant l'inscription
        self.hide()
        register_dlg = RegisterWindow(self)  # passer self comme parent
        result = register_dlg.exec()
        # Après fermeture de la fenêtre d'inscription, on réaffiche le login
        self.show()
        # Si l'inscription a réussi, on peut éventuellement connecter automatiquement
        if result == RegisterWindow.DialogCode.Accepted:
            # Option : remplir les champs email/password avec les nouvelles infos ?
            # Par défaut, on laisse l'utilisateur se connecter manuellement
            pass