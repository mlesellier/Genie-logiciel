#Système de gestion des congés
from datetime import date
from enum import Enum

# Enum pour les statuts des demandes
class StatutDemande(Enum):
    EN_ATTENTE = "En attente"
    VALIDEE = "Validée"
    REFUSEE = "Refusée"

# Classe TypeConge pour gérer les types de congés
class TypeConge:
    def __init__(self, nom, duree_max):
        self.nom = nom
        self.duree_max = duree_max

    def __str__(self):
        return f"{self.nom} (Durée maximale: {self.duree_max} jours)"

# Classe Employe
class Employe:
    def __init__(self, id, nom, poste):
        self.id = id
        self.nom = nom
        self.poste = poste
        self.demandes_conge = []

    def soumettre_demande(self, demande):
        self.demandes_conge.append(demande)

# Classe Manager (hérite d'Employe)
class Manager(Employe):
    def __init__(self, id, nom, poste):
        super().__init__(id, nom, poste)
        self.subordonnes = []

    def valider_demande(self, demande):
        if demande.statut == StatutDemande.EN_ATTENTE:
            demande.statut = StatutDemande.VALIDEE
        else:
            print("Demande déjà traitée.")
    
    def refuser_demande(self, demande):
        if demande.statut == StatutDemande.EN_ATTENTE:
            demande.statut = StatutDemande.REFUSEE
        else:
            print("Demande déjà traitée.")

# Classe RH (hérite d'Employe)
class RH(Employe):
    def __init__(self, id, nom, poste):
        super().__init__(id, nom, poste)

    def suivre_conges(self):
        for demande in self.demandes_conge:
            print(f"{demande.employe.nom}: {demande.type_conge.nom} - {demande.statut.value}")

# Classe DemandeConge
class DemandeConge:
    def __init__(self, employe, type_conge, date_debut, date_fin):
        self.employe = employe
        self.type_conge = type_conge
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.statut = StatutDemande.EN_ATTENTE

    def calculer_duree(self):
        return (self.date_fin - self.date_debut)

