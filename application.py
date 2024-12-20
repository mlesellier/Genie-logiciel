# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 17:24:49 2024

@author: villo
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QComboBox, QTableWidget, QTableWidgetItem,
    QWidget, QMessageBox, QDateEdit, QDialog
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDate
import beta  # Importation du script "beta" pour les fonctionnalités


class UserDetailsDialog(QDialog):
    """
    Fenêtre affichant tous les utilisateurs, leurs rôles et leurs dernières demandes de congé.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Détails des Utilisateurs")
        self.setGeometry(150, 150, 600, 400)

        # Définir une icône pour cette fenêtre
        self.setWindowIcon(QIcon("users_icon.png"))

        # Appliquer le style royal
        self.setStyleSheet(self.get_style())

        self.init_ui()

    def init_ui(self):
        # Layout principal
        layout = QVBoxLayout()

        # Tableau pour afficher les informations des utilisateurs
        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Nom", "Rôle", "Dernier congé"])
        layout.addWidget(self.table)

        # Charger les données des utilisateurs
        self.charger_utilisateurs()

        self.setLayout(layout)

    def charger_utilisateurs(self):
        """
        Charge les utilisateurs et leur dernière demande de congé dans le tableau.
        """
        data = beta.load_data()  # Charger les données depuis le fichier JSON
        utilisateurs = data["utilisateurs"]
        conges = data["conges"]

        self.table.setRowCount(0)  # Réinitialiser le tableau

        for utilisateur in utilisateurs:
            # Trouver le dernier congé de l'utilisateur
            dernier_conge = next(
                (c for c in sorted(conges, key=lambda x: x["date_debut"], reverse=True)
                 if c["utilisateur_id"] == utilisateur["id"]),
                None
            )
            dernier_conge_info = (
                f"{dernier_conge['type']} ({dernier_conge['date_debut']} - {dernier_conge['date_fin']})"
                if dernier_conge else "Aucun"
            )

            # Ajouter une ligne au tableau
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(utilisateur["nom"]))
            self.table.setItem(row, 1, QTableWidgetItem(utilisateur["role"]))
            self.table.setItem(row, 2, QTableWidgetItem(dernier_conge_info))

    def get_style(self):
        """
        Retourne le style royal en CSS.
        """
        return """
        QDialog {
            background-color: #1e3a66;
            color: #f1c40f;
        }
        QTableWidget {
            border: 2px solid #f1c40f;
            background-color: #ffffff;
            color: #1e3a66;
        }
        QHeaderView::section {
            background-color: #f1c40f;
            color: #1e3a66;
            font-weight: bold;
        }
        """


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Congés")
        self.setGeometry(100, 100, 800, 600)

        # Définir une icône pour la fenêtre principale
        self.setWindowIcon(QIcon("main_icon.png"))

        # Appliquer le style royal
        self.setStyleSheet(self.get_style())

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

        self.type_conge_input = QComboBox(self)
        self.type_conge_input.addItems(["Vacances", "RTT", "Maladie", "Mariage", "Décès", "Autre"])
        self.custom_conge_input = QLineEdit(self)
        self.custom_conge_input.setPlaceholderText("Si 'Autre', précisez ici")

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

        # Section : Afficher les demandes de congés
        layout.addWidget(QLabel("Demandes de congés"))
        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Type", "Début", "Fin", "Statut"])
        self.table.setSelectionBehavior(self.table.SelectRows)
        self.table.setSelectionMode(self.table.SingleSelection)
        layout.addWidget(self.table)

        # Boutons pour traiter une demande
        process_layout = QHBoxLayout()
        validate_button = QPushButton("Valider")
        validate_button.clicked.connect(self.valider_demande)
        refuse_button = QPushButton("Refuser")
        refuse_button.clicked.connect(self.refuser_demande)
        process_layout.addWidget(validate_button)
        process_layout.addWidget(refuse_button)
        layout.addLayout(process_layout)

        # Bouton : Afficher les détails des utilisateurs
        user_details_button = QPushButton("Afficher les utilisateurs")
        user_details_button.clicked.connect(self.afficher_utilisateurs)
        layout.addWidget(user_details_button)

        # Configuration principale
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Charger les données en temps réel
        self.charger_demandes()

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
                self.charger_demandes()
            else:
                QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs obligatoires.")
        except ValueError:
            QMessageBox.warning(self, "Erreur", "ID Utilisateur doit être un entier valide.")

    def charger_demandes(self):
        self.table.setRowCount(0)
        conges = beta.consulter_conges(role="RH")
        for conge in conges:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(conge["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(conge["type"]))
            self.table.setItem(row, 2, QTableWidgetItem(conge["date_debut"]))
            self.table.setItem(row, 3, QTableWidgetItem(conge["date_fin"]))
            self.table.setItem(row, 4, QTableWidgetItem(conge["statut"]))

    def valider_demande(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            conge_id = int(self.table.item(selected_row, 0).text())
            beta.traiter_demande_conge(conge_id, "Validé")
            QMessageBox.information(self, "Succès", "Demande validée.")
            self.charger_demandes()
        else:
            QMessageBox.warning(self, "Erreur", "Aucune demande sélectionnée.")

    def refuser_demande(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            conge_id = int(self.table.item(selected_row, 0).text())
            beta.traiter_demande_conge(conge_id, "Refusé")
            QMessageBox.information(self, "Succès", "Demande refusée.")
            self.charger_demandes()
        else:
            QMessageBox.warning(self, "Erreur", "Aucune demande sélectionnée.")

    def afficher_utilisateurs(self):
        dialog = UserDetailsDialog()
        dialog.exec_()

    def get_style(self):
        """
        Retourne le style royal en CSS avec des couleurs délavées.
        """
        return """
        QMainWindow {
            background-color: #2c496f; /* Bleu délavé */
            color: #d9c785; /* Doré délavé */
        }
        QLabel, QTableWidget {
            font-family: 'Georgia', serif;
            font-size: 14px;
            color: #d9c785; /* Doré délavé */
        }
        QLineEdit, QComboBox, QDateEdit {
            border: 2px solid #d9c785; /* Doré délavé */
            border-radius: 5px;
            padding: 5px;
            background-color: #f5f5f5; /* Blanc cassé */
            color: #2c496f; /* Bleu délavé */
        }
        QPushButton {
            background-color: #d9c785; /* Doré délavé */
            color: #2c496f; /* Bleu délavé */
            border-radius: 10px;
            padding: 10px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #c4b374; /* Doré légèrement plus foncé */
        }
        QTableWidget {
            background-color: #ffffff; /* Blanc */
            color: #2c496f; /* Bleu délavé */
            border: 2px solid #d9c785; /* Doré délavé */
        }
        QHeaderView::section {
            background-color: #d9c785; /* Doré délavé */
            color: #2c496f; /* Bleu délavé */
            font-weight: bold;
        }
        """

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())


