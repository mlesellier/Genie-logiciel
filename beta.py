# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 17:24:49 2024

@author: villo
"""

import json
import os

# Fichier JSON pour la "base de données"
DB_FILE = "conges_db.json"


# Fonction pour charger les données depuis le fichier JSON
def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as file:
            return json.load(file)
    else:
        return {"utilisateurs": [], "conges": [], "jours_feries": []}


# Fonction pour sauvegarder les données dans le fichier JSON
def save_data(data):
    with open(DB_FILE, "w") as file:
        json.dump(data, file, indent=4)


# Initialisation des données
db = load_data()


# Fonctionnalité : Ajouter un utilisateur
def ajouter_utilisateur(nom, email, role):
    """
    Ajoute un nouvel utilisateur au système (Employé, Manager ou RH).
    """
    user_id = len(db["utilisateurs"]) + 1
    db["utilisateurs"].append({
        "id": user_id,
        "nom": nom,
        "email": email,
        "role": role
    })
    save_data(db)


# Fonctionnalité : Ajouter une demande de congé
def ajouter_demande_conge(utilisateur_id, type_conge, date_debut, date_fin, motif=""):
    """
    Permet à un employé de saisir une demande de congé.
    """
    conge_id = len(db["conges"]) + 1
    db["conges"].append({
        "id": conge_id,
        "utilisateur_id": utilisateur_id,
        "type": type_conge,
        "date_debut": date_debut,
        "date_fin": date_fin,
        "motif": motif,
        "statut": "En attente"
    })
    save_data(db)


# Fonctionnalité : Valider ou refuser une demande de congé
def traiter_demande_conge(conge_id, statut):
    """
    Permet au manager de valider ou refuser une demande de congé.
    """
    for conge in db["conges"]:
        if conge["id"] == conge_id:
            conge["statut"] = statut
            save_data(db)
            return True
    return False


# Fonctionnalité : Consulter les congés
def consulter_conges(utilisateur_id=None, role="Employé"):
    """
    Affiche les congés en fonction du rôle (Employé, Manager, RH).
    """
    if role == "RH":
        return db["conges"]
    elif role == "Manager":
        # Exemple simplifié : retourne toutes les demandes (devrait filtrer par équipe)
        return db["conges"]
    elif role == "Employé" and utilisateur_id:
        return [c for c in db["conges"] if c["utilisateur_id"] == utilisateur_id]
    else:
        return []


# Fonctionnalité : Ajouter un jour férié
def ajouter_jour_ferie(date, description):
    """
    Permet au RH d'ajouter un jour férié.
    """
    db["jours_feries"].append({
        "date": date,
        "description": description
    })
    save_data(db)


# Exemple d'utilisation
if __name__ == "__main__":
    # Ajouter des utilisateurs
    ajouter_utilisateur("Alice", "alice@example.com", "Employé")
    ajouter_utilisateur("Bob", "bob@example.com", "Manager")
    ajouter_utilisateur("Claire", "claire@example.com", "RH")

    # Ajouter une demande de congé
    ajouter_demande_conge(utilisateur_id=1, type_conge="Vacances", date_debut="2024-12-25", date_fin="2025-01-01")

    # Valider une demande de congé
    traiter_demande_conge(conge_id=1, statut="Validé")

    # Ajouter un jour férié
    ajouter_jour_ferie(date="2024-12-25", description="Noël")

    # Consulter les congés pour RH
    print("Congés (RH) :", consulter_conges(role="RH"))

