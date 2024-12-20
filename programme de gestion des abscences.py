from datetime import date, timedelta

# Classes principales
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

# Programme principal
def main():
    # Initialisation des données
    employe = Employe(1, "Alice", 20)
    manager = Manager()
    rh = RH()

    # Exemple 1 : Soumission d'une demande de congé
    demande = DemandeConge(1, "Vacances", date.today(), date.today() + timedelta(days=4), employe)
    print(f"Demande initiale : {demande.etat}")

    # Exemple 2 : Validation par le manager
    manager.valider_demande(demande)
    print(f"Demande après validation : {demande.etat}")
    print(f"Solde de congés restant : {employe.solde_conges} jours")

    # Exemple 3 : Refus d'une nouvelle demande
    nouvelle_demande = DemandeConge(2, "RTT", date.today() + timedelta(days=10), date.today() + timedelta(days=12), employe)
    manager.refuser_demande(nouvelle_demande)
    print(f"Nouvelle demande : {nouvelle_demande.etat}")

    # Exemple 4 : Modification des règles par la RH
    nouvelles_regles = {"jours_vacances": 25, "jours_rtt": 12}
    regles = rh.modifier_regles(nouvelles_regles)
    print(f"Nouvelles règles : Vacances = {regles['jours_vacances']}, RTT = {regles['jours_rtt']}")

if __name__ == "__main__":
    main()
