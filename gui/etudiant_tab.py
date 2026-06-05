import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QInputDialog,
                             QMessageBox, QHeaderView, QComboBox, QDialog,
                             QLabel, QDialogButtonBox, QLineEdit, QSpinBox, QFormLayout)
from PyQt6.QtCore import Qt
from database import get_session
from src.services.etudiant_service import EtudiantService
from src.schemas.etudiant import EtudiantCreate, EtudiantUpdate, SexeEnum, FiliereEnum, GradeEnum
from src.desktop_session import get_current_user_from_token

class EtudiantFormDialog(QDialog):
    """Dialogue unique pour ajouter ou modifier un étudiant."""
    def __init__(self, parent=None, etudiant=None):
        super().__init__(parent)
        self.etudiant = etudiant  # None pour ajout, sinon objet existant
        self.setWindowTitle("Modifier un étudiant" if etudiant else "Ajouter un étudiant")
        self.setModal(True)
        self.setMinimumWidth(350)

        layout = QFormLayout(self)

        # Nom
        self.nom_edit = QLineEdit()
        if etudiant:
            self.nom_edit.setText(etudiant.nom)
        layout.addRow("Nom :", self.nom_edit)

        # Âge
        self.age_spin = QSpinBox()
        self.age_spin.setRange(0, 120)
        if etudiant:
            self.age_spin.setValue(etudiant.age)
        else:
            self.age_spin.setValue(18)
        layout.addRow("Âge :", self.age_spin)

        # Sexe
        self.sexe_combo = QComboBox()
        self.sexe_combo.addItems([s.value for s in SexeEnum])
        if etudiant:
            self.sexe_combo.setCurrentText(etudiant.sexe.value)
        layout.addRow("Sexe :", self.sexe_combo)

        # Filière
        self.filiere_combo = QComboBox()
        self.filiere_combo.addItems([f.value for f in FiliereEnum])
        if etudiant:
            self.filiere_combo.setCurrentText(etudiant.filiere.value)
        layout.addRow("Filière :", self.filiere_combo)

        # Grade
        self.grade_combo = QComboBox()
        self.grade_combo.addItems([g.value for g in GradeEnum])
        if etudiant:
            self.grade_combo.setCurrentText(etudiant.grade.value)
        layout.addRow("Grade :", self.grade_combo)

        # Boutons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def get_data(self):
        """Retourne un tuple (nom, age, sexe, filiere, grade) ou None si invalide."""
        nom = self.nom_edit.text().strip()
        if not nom:
            return None
        age = self.age_spin.value()
        sexe = SexeEnum(self.sexe_combo.currentText())
        filiere = FiliereEnum(self.filiere_combo.currentText())
        grade = GradeEnum(self.grade_combo.currentText())
        return nom, age, sexe, filiere, grade


class EtudiantTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Nom", "Âge", "Sexe", "Filière", "Grade", "Propriétaire"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton(" Ajouter")
        self.add_btn.clicked.connect(self.add_etudiant)
        self.edit_btn = QPushButton("Modifier")
        self.edit_btn.clicked.connect(self.edit_etudiant)
        self.delete_btn = QPushButton("Supprimer")
        self.delete_btn.clicked.connect(self.delete_etudiant)
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
                QMessageBox.warning(self, "Erreur", "Session expirée")
                return
            etudiants = EtudiantService.get_etudiants_by_owner(session, current_user.id)
        self.table.setRowCount(len(etudiants))
        for i, e in enumerate(etudiants):
            self.table.setItem(i, 0, QTableWidgetItem(str(e.id)))
            self.table.setItem(i, 1, QTableWidgetItem(e.nom))
            self.table.setItem(i, 2, QTableWidgetItem(str(e.age)))
            self.table.setItem(i, 3, QTableWidgetItem(e.sexe.value))
            self.table.setItem(i, 4, QTableWidgetItem(e.filiere.value))
            self.table.setItem(i, 5, QTableWidgetItem(e.grade.value))
            self.table.setItem(i, 6, QTableWidgetItem(str(e.owner_id)))
        self.table.resizeRowsToContents()

    def add_etudiant(self):
        dlg = EtudiantFormDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.get_data()
            if not data:
                QMessageBox.warning(self, "Erreur", "Le nom ne peut pas être vide")
                return
            nom, age, sexe, filiere, grade = data
            with next(get_session()) as session:
                current_user = get_current_user_from_token(session)
                if not current_user:
                    QMessageBox.warning(self, "Erreur", "Session expirée")
                    return
                create_data = EtudiantCreate(nom=nom, age=age, sexe=sexe, filiere=filiere, grade=grade)
                EtudiantService.create_etudiant(session, create_data, current_user.id)
            self.load_data()
            QMessageBox.information(self, "Succès", "Étudiant ajouté avec succès")

    def edit_etudiant(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Erreur", "Sélectionnez un étudiant")
            return
        e_id = int(self.table.item(row, 0).text())
        with next(get_session()) as session:
            current_user = get_current_user_from_token(session)
            if not current_user:
                QMessageBox.warning(self, "Erreur", "Session expirée")
                return
            etu = EtudiantService.get_etudiant(session, e_id)
            if etu.owner_id != current_user.id:
                QMessageBox.warning(self, "Erreur", "Pas autorisé")
                return
            dlg = EtudiantFormDialog(self, etudiant=etu)
            if dlg.exec() == QDialog.DialogCode.Accepted:
                data = dlg.get_data()
                if not data:
                    QMessageBox.warning(self, "Erreur", "Le nom ne peut pas être vide")
                    return
                nom, age, sexe, filiere, grade = data
                update_data = EtudiantUpdate(nom=nom, age=age, sexe=sexe, filiere=filiere, grade=grade)
                EtudiantService.update_etudiant(session, etu, update_data)
                self.load_data()
                QMessageBox.information(self, "Succès", "Étudiant modifié avec succès")

    def delete_etudiant(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Erreur", "Sélectionnez un étudiant")
            return
        e_id = int(self.table.item(row, 0).text())
        confirm = QMessageBox.question(self, "Supprimer", "Confirmer la suppression ?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            with next(get_session()) as session:
                current_user = get_current_user_from_token(session)
                if not current_user:
                    QMessageBox.warning(self, "Erreur", "Session expirée")
                    return
                etu = EtudiantService.get_etudiant(session, e_id)
                if etu.owner_id != current_user.id:
                    QMessageBox.warning(self, "Erreur", "Pas autorisé")
                    return
                EtudiantService.delete_etudiant(session, e_id)
            self.load_data()