# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 17:24:49 2024

@author: villo
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QComboBox, QTextEdit, QWidget, QMessageBox, QDateEdit
)
from PyQt5.QtCore import QDate
import beta  # Importation du script "beta" pour les fonctionnalités


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Congés")
        self.setGeometry(100, 100, 700, 400)
        self.init_ui()

    def init_ui(self):
        # Layout principal
        layout = QVBoxLayout()

        # Section : Ajouter un utilisateur
        layout.addWidget(QLabel("Ajouter un utilisateur"))
        self.nom_input = QLineEdit(self)
        self.nom_input.setPlaceholderText("Nom")
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Email")
        self.role_input = QComboBox(self)
        self.role_input.addItems(["Employé", "Manager", "RH"])
        add_user_button = QPushButton("Ajouter utilisateur")
        add_user_button.clicked.connect(self.ajouter_utilisateur)

        user_layout = QHBoxLayout()
        user_layout.addWidget(self.nom_input)
        user_layout.addWidget(self.email_input)
        user_layout.addWidget(self.role_input)
        user_layout.addWidget(add_user_button)
        layout.addLayout(user_layout)

        # Section : Ajouter une demande de congé
        layout.addWidget(QLabel("Ajouter une demande de congé"))
        self.user_id_input = QLineEdit(self)
        self.user_id_input.setPlaceholderText("ID Utilisateur")

        # Menu déroulant pour type de congé
        self.type_conge_input = QComboBox(self)
        self.type_conge_input.addItems(["Vacances", "RTT", "Maladie", "Mariage", "Décès", "Autre"])
        self.custom_conge_input = QLineEdit(self)
        self.custom_conge_input.setPlaceholderText("Si 'Autre', précisez ici")

        # Sélecteurs de date pour début et fin
        self.date_debut_input = QDateEdit(self)
        self.date_debut_input.setCalendarPopup(True)
        self.date_debut_input.setDate(QDate.currentDate())

        self.date_fin_input = QDateEdit(self)
        self.date_fin_input.setCalendarPopup(True)
        self.date_fin_input.setDate(QDate.currentDate())

        self.motif_input = QLineEdit(self)
        self.motif_input.setPlaceholderText("Motif (optionnel)")
        add_leave_button = QPushButton("Ajouter demande")
        add_leave_button.clicked.connect(self.ajouter_demande_conge)

        leave_layout = QHBoxLayout()
        leave_layout.addWidget(self.user_id_input)
        leave_layout.addWidget(self.type_conge_input)
        leave_layout.addWidget(self.custom_conge_input)
        leave_layout.addWidget(self.date_debut_input)
        leave_layout.addWidget(self.date_fin_input)
        leave_layout.addWidget(self.motif_input)
        leave_layout.addWidget(add_leave_button)
        layout.addLayout(leave_layout)

        # Section : Afficher les congés
        display_conges_button = QPushButton("Afficher les congés")
        display_conges_button.clicked.connect(self.afficher_conges)
        self.conges_display = QTextEdit(self)
        self.conges_display.setReadOnly(True)

        layout.addWidget(display_conges_button)
        layout.addWidget(self.conges_display)

        # Configuration principale
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def ajouter_utilisateur(self):
        nom = self.nom_input.text()
        email = self.email_input.text()
        role = self.role_input.currentText()
        if nom and email:
            beta.ajouter_utilisateur(nom, email, role)
            QMessageBox.information(self, "Succès", "Utilisateur ajouté avec succès.")
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs.")

    def ajouter_demande_conge(self):
        try:
            utilisateur_id = int(self.user_id_input.text())
            type_conge = self.type_conge_input.currentText()
            if type_conge == "Autre":
                type_conge = self.custom_conge_input.text()

            date_debut = self.date_debut_input.date().toString("yyyy-MM-dd")
            date_fin = self.date_fin_input.date().toString("yyyy-MM-dd")
            motif = self.motif_input.text()

            if type_conge and date_debut and date_fin:
                beta.ajouter_demande_conge(utilisateur_id, type_conge, date_debut, date_fin, motif)
                QMessageBox.information(self, "Succès", "Demande de congé ajoutée avec succès.")
            else:
                QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs obligatoires.")
        except ValueError:
            QMessageBox.warning(self, "Erreur", "ID Utilisateur doit être un entier valide.")

    def afficher_conges(self):
        conges = beta.consulter_conges(role="RH")  # Par défaut, affiche tous les congés
        if conges:
            display_text = "\n".join(
                [f"ID: {c['id']}, Type: {c['type']}, Début: {c['date_debut']}, Fin: {c['date_fin']}, Statut: {c['statut']}" for c in conges]
            )
        else:
            display_text = "Aucun congé enregistré."
        self.conges_display.setText(display_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())

