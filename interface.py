import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QComboBox, QDateEdit, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect

class DemandeCongeWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Initialisation de la fenêtre principale
        self.setWindowTitle("Soumettre une Demande de Congé")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: #f7f7f7;")  # Couleur de fond douce et claire

        # Ajout d'une icône pour la fenêtre
        self.setWindowIcon(QIcon("icon.png"))  # Assurez-vous d'avoir un fichier icon.png dans votre répertoire

        # Création du layout principal
        self.layout = QVBoxLayout()

        # Initialisation du formulaire pour saisir les informations
        self.form_layout = QFormLayout()

        # Champ ID Employé avec un validateur de texte numérique
        self.employe_id_input = QLineEdit(self)
        self.employe_id_input.setValidator(QRegExpValidator(QRegExp(r"^\d+$")))
        self.employe_id_input.setPlaceholderText("ID Employé (Numérique)")

        # Champ Date de Début avec un sélecteur de date au format français
        self.date_debut_input = QDateEdit(self)
        self.date_debut_input.setDate(QDate.currentDate())
        self.date_debut_input.setDisplayFormat("dd/MM/yyyy")  # Format de la date en français
        self.date_debut_input.setCalendarPopup(True)

        # Champ Date de Fin avec un sélecteur de date au format français
        self.date_fin_input = QDateEdit(self)
        self.date_fin_input.setDate(QDate.currentDate())
        self.date_fin_input.setDisplayFormat("dd/MM/yyyy")  # Format de la date en français
        self.date_fin_input.setCalendarPopup(True)

        # Champ Type de Congé (avec une liste déroulante)
        self.type_conge_input = QComboBox(self)
        self.type_conge_input.addItems(["Maladie", "Vacances", "Autre"])

        # Ajout des champs au formulaire
        self.form_layout.addRow("ID Employé:", self.employe_id_input)
        self.form_layout.addRow("Date de Début (jj/mm/aaaa):", self.date_debut_input)
        self.form_layout.addRow("Date de Fin (jj/mm/aaaa):", self.date_fin_input)
        self.form_layout.addRow("Type de Congé:", self.type_conge_input)

        # Ajout du formulaire au layout principal
        self.layout.addLayout(self.form_layout)

        # Bouton pour soumettre la demande avec un effet de survol
        self.submit_button = QPushButton("Soumettre la Demande", self)
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;  /* Vert */
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
                cursor: pointer;
            }
            QPushButton:pressed {
                background-color: #388e3c;
            }
        """)
        self.submit_button.clicked.connect(self.soumettre_demande)
        self.layout.addWidget(self.submit_button)

        # Label pour afficher les messages (succès ou erreur)
        self.message_label = QLabel("", self)
        self.layout.addWidget(self.message_label)

        # Ajout d'un effet de l'ombre pour donner un effet visuel agréable
        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setBlurRadius(20)
        shadow_effect.setOffset(5, 5)
        self.submit_button.setGraphicsEffect(shadow_effect)

        # Affichage des demandes de congé dans un tableau
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID Employé", "Date Début", "Date Fin", "Type de Congé"])
        self.layout.addWidget(self.table)

        # Charger les demandes sauvegardées
        self.load_demandes()

        # Définit le layout principal de la fenêtre
        self.setLayout(self.layout)

    def soumettre_demande(self):
        """
        Cette méthode est appelée lorsque l'utilisateur clique sur le bouton 'Soumettre la Demande'.
        Elle récupère les données du formulaire, vérifie leur validité, puis enregistre la demande localement.
        """

        # Récupérer les valeurs saisies par l'utilisateur dans le formulaire
        employe_id = self.employe_id_input.text()
        date_debut = self.date_debut_input.text()
        date_fin = self.date_fin_input.text()
        type_conge = self.type_conge_input.currentText()

        # Vérification que tous les champs sont remplis
        if not employe_id or not date_debut or not date_fin or not type_conge:
            self.message_label.setText("Tous les champs sont requis.")
            self.message_label.setStyleSheet("color: red; font-weight: bold;")
            return

        # Vérification du format des dates (jj/mm/aaaa)
        if not self.valider_date(date_debut) or not self.valider_date(date_fin):
            self.message_label.setText("Format des dates invalide. Utilisez jj/mm/aaaa.")
            self.message_label.setStyleSheet("color: red; font-weight: bold;")
            return

        # Sauvegarder la demande dans un fichier local
        demande = {
            "employeId": employe_id,
            "dateDebut": date_debut,
            "dateFin": date_fin,
            "typeConge": type_conge
        }
        self.save_demande(demande)

        # Affichage du message de succès
        self.message_label.setText("Demande soumise avec succès.")
        self.message_label.setStyleSheet("color: green; font-weight: bold;")

        # Recharger les demandes dans la table
        self.load_demandes()

    def save_demande(self, demande):
        """
        Sauvegarde une demande de congé dans un fichier local (JSON).
        """
        try:
            # Charger les demandes existantes
            with open("demandes_conge.json", "r") as file:
                demandes = json.load(file)
        except FileNotFoundError:
            demandes = []

        # Ajouter la nouvelle demande à la liste
        demandes.append(demande)

        # Sauvegarder la liste mise à jour
        with open("demandes_conge.json", "w") as file:
            json.dump(demandes, file, indent=4)

    def load_demandes(self):
        """
        Charge les demandes de congé sauvegardées et les affiche dans la table.
        """
        try:
            with open("demandes_conge.json", "r") as file:
                demandes = json.load(file)
        except FileNotFoundError:
            demandes = []

        # Vider la table avant de la remplir avec les nouvelles données
        self.table.setRowCount(0)

        # Ajouter les données à la table
        for demande in demandes:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(demande["employeId"]))
            self.table.setItem(row_position, 1, QTableWidgetItem(demande["dateDebut"]))
            self.table.setItem(row_position, 2, QTableWidgetItem(demande["dateFin"]))
            self.table.setItem(row_position, 3, QTableWidgetItem(demande["typeConge"]))

    def valider_date(self, date):
        """
        Valide le format de la date (jj/mm/aaaa).
        """
        try:
            day, month, year = map(int, date.split('/'))
            if 1 <= month <= 12 and 1 <= day <= 31 and len(str(year)) == 4:
                return True
            else:
                return False
        except ValueError:
            return False


if __name__ == "__main__":
    """
    Fonction principale qui initialise l'application PyQt5, crée la fenêtre et lance l'interface.
    """
    app = QApplication(sys.argv)  # Création de l'application PyQt5
    window = DemandeCongeWindow()  # Création de la fenêtre de demande de congé
    window.show()  # Affichage de la fenêtre
    sys.exit(app.exec_())  # Lancement de l'application et gestion des événements
