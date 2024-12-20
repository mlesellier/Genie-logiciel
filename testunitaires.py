import unittest
from datetime import date, timedelta

# Simulations des classes du système
class Employe:
    def __init__(self, id, nom, solde_conges):
        self.id = id
        self.nom = nom
        self.solde_conges = solde_conges

class DemandeConge:
    def __init__(self, id, type_conge, date_debut, date_fin, demandeur, etat="En attente"):
        self.id = id
        self.type_conge = type_conge
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.demandeur = demandeur
        self.etat = etat

class Manager:
    def valider_demande(self, demande):
        if demande.etat == "En attente":
            demande.etat = "Validée"
            demande.demandeur.solde_conges -= (demande.date_fin - demande.date_debut).days + 1
        return demande.etat

    def refuser_demande(self, demande):
        if demande.etat == "En attente":
            demande.etat = "Refusée"
        return demande.etat

class RH:
    def modifier_regles(self, nouvelles_regles):
        return nouvelles_regles

# Simulations des règles
class ReglesConge:
    def __init__(self, jours_vacances, jours_rtt):
        self.jours_vacances = jours_vacances
        self.jours_rtt = jours_rtt

# Test unitaire principal
class TestGestionConges(unittest.TestCase):
    def setUp(self):
        # Préparer les données de test
        self.employe = Employe(1, "Alice", 20)
        self.manager = Manager()
        self.rh = RH()
        self.demande = DemandeConge(1, "Vacances", date.today(), date.today() + timedelta(days=4), self.employe)

    # Tests Employé
    def test_soumission_valide(self):
        self.assertEqual(self.demande.etat, "En attente")

    def test_soumission_invalide(self):
        demande_invalide = DemandeConge(2, "Vacances", date.today() + timedelta(days=5), date.today(), self.employe)
        self.assertTrue(demande_invalide.date_debut > demande_invalide.date_fin, "Les dates sont invalides")

    # Tests Manager
    def test_validation_demande(self):
        etat_apres_validation = self.manager.valider_demande(self.demande)
        self.assertEqual(etat_apres_validation, "Validée")
        self.assertEqual(self.employe.solde_conges, 15)  # 20 - 5 jours validés

    def test_refus_demande(self):
        etat_apres_refus = self.manager.refuser_demande(self.demande)
        self.assertEqual(etat_apres_refus, "Refusée")

    # Tests RH
    def test_modifier_regles(self):
        nouvelles_regles = {"jours_vacances": 30, "jours_rtt": 10}
        regles_appliquees = self.rh.modifier_regles(nouvelles_regles)
        self.assertEqual(regles_appliquees["jours_vacances"], 30)
        self.assertEqual(regles_appliquees["jours_rtt"], 10)

if __name__ == "__main__":
    unittest.main()
