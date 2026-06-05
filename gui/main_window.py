from PyQt6.QtWidgets import (QMainWindow, QTabWidget, QMenuBar, QMenu,
                             QMessageBox, QStatusBar, QToolBar)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from gui.subject_tab import SubjectTab
from gui.etudiant_tab import EtudiantTab
from gui.styles import apply_stylesheet
from src.desktop_session import set_token, _current_token
from src.services.auth_service import AuthService
from database import get_session

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des matières et étudiants")
        self.setGeometry(100, 100, 1100, 700)
        apply_stylesheet(self)

        # Barre d'outils
        toolbar = self.addToolBar("Actions")
        toolbar.setMovable(False)
        logout_action = QAction(" Déconnexion", self)
        logout_action.triggered.connect(self.logout)
        toolbar.addAction(logout_action)

        # Onglets
        tabs = QTabWidget()
        self.subject_tab = SubjectTab()
        self.etudiant_tab = EtudiantTab()
        tabs.addTab(self.subject_tab, " Matières")
        tabs.addTab(self.etudiant_tab, " Étudiants")
        self.setCentralWidget(tabs)

        

        self.statusBar().showMessage("Connecté")

    def logout(self):
        reply = QMessageBox.question(self, "Déconnexion",
                                     "Voulez-vous vraiment vous déconnecter ?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            if _current_token:
                with next(get_session()) as session:
                    AuthService.blacklist_token(_current_token, session)
            set_token(None)
            self.close()  # ferme la fenêtre principale, on revient à la fenêtre de login