import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QMessageBox,
                             QHeaderView, QDialog, QFormLayout, QLineEdit,
                             QSpinBox, QDialogButtonBox)
from PyQt6.QtCore import Qt
from database import get_session
from src.services.subject_service import SubjectService
from src.schemas.subject import SubjectCreate, SubjectUpdate
from src.desktop_session import get_current_user_from_token


class SubjectFormDialog(QDialog):
    """Formulaire unique pour ajouter ou modifier une matière."""
    def __init__(self, parent=None, subject=None):
        super().__init__(parent)
        self.subject = subject
        self.setWindowTitle("Modifier la matière" if subject else "Ajouter une matière")
        self.setModal(True)
        layout = QFormLayout(self)

        self.nom_edit = QLineEdit()
        if subject:
            self.nom_edit.setText(subject.nom)
        layout.addRow("Nom :", self.nom_edit)

        self.matiere_edit = QLineEdit()
        if subject:
            self.matiere_edit.setText(subject.matiere)
        layout.addRow("Matière :", self.matiere_edit)

        self.coef_spin = QSpinBox()
        self.coef_spin.setRange(1, 100)
        if subject:
            self.coef_spin.setValue(subject.coefficient)
        layout.addRow("Coefficient :", self.coef_spin)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def get_data(self):
        """Retourne (nom, matiere, coefficient) ou None si validation échoue."""
        nom = self.nom_edit.text().strip()
        if not nom:
            return None
        matiere = self.matiere_edit.text().strip()
        if not matiere:
            return None
        coef = self.coef_spin.value()
        return nom, matiere, coef


class SubjectTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Nom", "Matière", "Coefficient", "Propriétaire"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton(" Ajouter")
        self.add_btn.clicked.connect(self.add_subject)
        self.edit_btn = QPushButton(" Modifier")
        self.edit_btn.clicked.connect(self.edit_subject)
        self.delete_btn = QPushButton(" Supprimer")
        self.delete_btn.clicked.connect(self.delete_subject)
        self.refresh_btn = QPushButton(" Actualiser")
        self.refresh_btn.clicked.connect(self.load_data)
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.refresh_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        with next(get_session()) as session:
            current_user = get_current_user_from_token(session)
            if not current_user:
                QMessageBox.warning(self, "Erreur", "Session expirée, veuillez vous reconnecter")
                return
            subjects = SubjectService.get_subjects_by_owner(session, current_user.id)
        self.table.setRowCount(len(subjects))
        for i, subj in enumerate(subjects):
            self.table.setItem(i, 0, QTableWidgetItem(str(subj.id)))
            self.table.setItem(i, 1, QTableWidgetItem(subj.nom))
            self.table.setItem(i, 2, QTableWidgetItem(subj.matiere))
            self.table.setItem(i, 3, QTableWidgetItem(str(subj.coefficient)))
            self.table.setItem(i, 4, QTableWidgetItem(str(subj.owner_id)))
        self.table.resizeRowsToContents()

    def add_subject(self):
        dialog = SubjectFormDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if data is None:
                QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs")
                return
            nom, matiere, coef = data
            with next(get_session()) as session:
                current_user = get_current_user_from_token(session)
                if not current_user:
                    QMessageBox.warning(self, "Erreur", "Session expirée")
                    return
                create_data = SubjectCreate(nom=nom, matiere=matiere, coefficient=coef)
                SubjectService.create_subject(session, create_data, current_user.id)
            self.load_data()

    def edit_subject(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une matière")
            return
        subj_id = int(self.table.item(row, 0).text())
        with next(get_session()) as session:
            current_user = get_current_user_from_token(session)
            if not current_user:
                QMessageBox.warning(self, "Erreur", "Session expirée")
                return
            subj = SubjectService.get_subject(session, subj_id)
            if subj.owner_id != current_user.id:
                QMessageBox.warning(self, "Erreur", "Vous n'êtes pas autorisé à modifier cette matière")
                return
            dialog = SubjectFormDialog(self, subject=subj)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_data()
                if data is None:
                    QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs")
                    return
                nom, matiere, coef = data
                update = SubjectUpdate(nom=nom, matiere=matiere, coefficient=coef)
                SubjectService.update_subject(session, subj, update)
                self.load_data()

    def delete_subject(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une matière")
            return
        subj_id = int(self.table.item(row, 0).text())
        confirm = QMessageBox.question(self, "Supprimer", "Confirmer la suppression ?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            with next(get_session()) as session:
                current_user = get_current_user_from_token(session)
                if not current_user:
                    QMessageBox.warning(self, "Erreur", "Session expirée")
                    return
                subj = SubjectService.get_subject(session, subj_id)
                if subj.owner_id != current_user.id:
                    QMessageBox.warning(self, "Erreur", "Pas autorisé")
                    return
                SubjectService.delete_subject(session, subj_id)
            self.load_data()