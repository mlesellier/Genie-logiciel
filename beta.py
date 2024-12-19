# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 17:24:49 2024

@author: villo
"""

import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QTableWidget, QVBoxLayout, QWidget

# Connexion à la base de données SQLite
# Base de données utilisée pour stocker les utilisateurs, congés, et jours fériés
conn = sqlite3.connect("gestion_conges.db")
cursor = conn.cursor()

# Création des tables nécessaires
cursor.execute("""
CREATE TABLE IF NOT EXISTS utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    email TEXT,
    role TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS conges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    date_debut TEXT,
    date_fin TEXT,
    statut TEXT,
    utilisateur_id INTEGER,
    FOREIGN KEY(utilisateur_id) REFERENCES utilisateurs(id)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS jours_feries (
    date TEXT PRIMARY KEY,
    description TEXT
)
""")
conn.commit()


class GestionCongesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Congés")
        self.setGeometry(100, 100, 800, 600)

        # Authentification des utilisateurs
        # Page d'accueil : Saisie du nom et rôle pour se connecter
        self.login_label = QLabel("Nom :", self)
        self.login_label.move(50, 50)
        self.login_input = QLineEdit(self)
        self.login_input.move(120, 50)

        self.role_label = QLabel("Rôle :", self)
        self.role_label.move(50, 100)
        self.role_input = QLineEdit(self)
        self.role_input.move(120, 100)

        self.login_button = QPushButton("Se connecter", self)
        self.login_button.move(120, 150)
        self.login_button.clicked.connect(self.auth_user)

    def auth_user(self):
        # Authentification basée sur les données saisies
        nom = self.login_input.text()
        role = self.role_input.text()
        cursor.execute("SELECT * FROM utilisateurs WHERE nom = ? AND role = ?", (nom, role))
        user = cursor.fetchone()

        if user:
            self.show_main_menu(role)
        else:
            self.show_message("Utilisateur non trouvé. Veuillez vérifier les informations.")

    def show_main_menu(self, role):
        # Affichage du menu principal selon le rôle
        if role == "Employé":
            self.show_employe_menu()
        elif role == "Manager":
            self.show_manager_menu()
        elif role == "RH":
            self.show_rh_menu()

    def show_employe_menu(self):
        # Interface pour saisir une demande de congé
        self.clear_screen()
        self.conge_type_label = QLabel("Type de congé :", self)
        self.conge_type_label.move(50, 50)
        self.conge_type_input = QLineEdit(self)
        self.conge_type_input.move(150, 50)

        self.date_debut_label = QLabel("Date début :", self)
        self.date_debut_label.move(50, 100)
        self.date_debut_input = QLineEdit(self)
        self.date_debut_input.move(150, 100)

        self.date_fin_label = QLabel("Date fin :", self)
        self.date_fin_label.move(50, 150)
        self.date_fin_input = QLineEdit(self)
        self.date_fin_input.move(150, 150)

        self.submit_button = QPushButton("Soumettre", self)
        self.submit_button.move(150, 200)
        self.submit_button.clicked.connect(self.submit_conge)

    def submit_conge(self):
        # Enregistrement de la demande de congé
        type_conge = self.conge_type_input.text()
        date_debut = self.date_debut_input.text()
        date_fin = self.date_fin_input.text()

        cursor.execute("""
        INSERT INTO conges (type, date_debut, date_fin, statut, utilisateur_id) 
        VALUES (?, ?, ?, 'En attente', ?)
        """, (type_conge, date_debut, date_fin, 1))  # 1 : ID utilisateur fictif
        conn.commit()
        self.show_message("Demande de congé soumise avec succès.")

    def show_manager_menu(self):
        # Interface pour gérer les validations de congés
        self.clear_screen()
        self.label = QLabel("Validation des congés (en attente)", self)
        self.label.move(50, 50)

        self.table = QTableWidget(self)
        self.table.move(50, 100)
        self.table.resize(700, 400)

        # Charger les demandes de congés en attente
        cursor.execute("SELECT * FROM conges WHERE statut = 'En attente'")
        demandes = cursor.fetchall()
        self.table.setRowCount(len(demandes))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Type", "Date début", "Date fin", "Action"])

    def show_rh_menu(self):
        # Interface pour suivre les congés et gérer les jours fériés
        self.clear_screen()
        self.label = QLabel("Gestion RH - Congés et jours fériés", self)
        self.label.move(50, 50)

        self.add_jour_ferie_button = QPushButton("Ajouter un jour férié", self)
        self.add_jour_ferie_button.move(50, 100)
        self.add_jour_ferie_button.clicked.connect(self.add_jour_ferie)

    def add_jour_ferie(self):
        # Ajout de jours fériés
        self.clear_screen()
        self.label = QLabel("Date du jour férié (YYYY-MM-DD) :", self)
        self.label.move(50, 50)
        self.input = QLineEdit(self)
        self.input.move(250, 50)

        self.submit_button = QPushButton("Ajouter", self)
        self.submit_button.move(50, 100)
        self.submit_button.clicked.connect(self.save_jour_ferie)

    def save_jour_ferie(self):
        # Enregistrement du jour férié
        date = self.input.text()
        cursor.execute("INSERT INTO jours_feries (date, description) VALUES (?, ?)", (date, "Jour férié"))
        conn.commit()
        self.show_message("Jour férié ajouté avec succès.")

    def show_message(self, message):
        # Affichage d'un message générique
        self.message_label = QLabel(message, self)
        self.message_label.move(50, 250)
        self.message_label.show()

    def clear_screen(self):
        # Effacer tous les widgets de l'écran
        for widget in self.findChildren(QWidget):
            widget.deleteLater()


# Lancer l'application
app = QApplication([])
window = GestionCongesApp()
window.show()
app.exec_()
