class Utilisateur:
    def __init__(self, id, nom, prenom, email, mot_de_passe):
        self._id = id
        self._nom = nom
        self._prenom = prenom
        self._email = email
        self.__mot_de_passe = mot_de_passe

    def get_nom(self):
        return self._nom

    def set_nom(self, nom):
        self._nom = nom

    def get_email(self):
        return self._email

    def set_email(self, email):
        self._email = email


class Manager(Utilisateur):
    def valider_demande(self, demande):
        if demande.statut == "En attente":
            demande.statut = "Approuvé"
            print(f"Demande approuvée pour {demande.employe.get_nom()}.")
        else:
            print("Demande déjà traitée.")

    def consulter_demandes_equipe(self, demandes):
        for demande in demandes:
            if demande.employe._id == self._id:
                print(f"Demande de {demande.employe.get_nom()} : {demande.statut}")

class RessourcesHumaines(Utilisateur):
    def consulter_toutes_les_demandes(self, demandes):
        for demande in demandes:
            print(f"Demande de {demande.employe.get_nom()} : {demande.statut}")

    def gerer_types_conge(self, types_conge):
        for type_conge in types_conge:
            print(f"Type : {type_conge.libelle} - {type_conge.description}")


class DemandeConge:
    def __init__(self, employe, type_conge, date_debut, date_fin):
        self.employe = employe
        self.type_conge = type_conge
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.statut = "En attente"

    def soumettre(self):
        print(f"Demande soumise pour {self.employe.get_nom()} du {self.date_debut} au {self.date_fin}.")


class TypeConge:
    def __init__(self, id, libelle, description):
        self.id = id
        self.libelle = libelle
        self.description = description

# Initialisation des types de congés
types_conge = [
    TypeConge(1, "Vacances", "Congés pour vacances annuelles"),
    TypeConge(2, "RTT", "Réduction du temps de travail"),
    TypeConge(3, "Congés Maladie", "Congés pour raison de santé"),
    TypeConge(4, "Jours Fériés", "Jours fériés nationaux"),
    TypeConge(5, "Congés de Droit", "Congés pour mariage, naissance, etc."),
]

# Exemple d'utilisation
for type_conge in types_conge:
    print(f"{type_conge.libelle}: {type_conge.description}")
