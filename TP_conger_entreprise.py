## 4) Implanter les principales fonctionnalités

from random import randint

#type de congés
def type_de_conger():
    conger = int(input("Entrer le type de congé:\n1)vacances\n2)RTT\n3)congés maladie\n4)jour fériés\n5)congés de droit\n6)mariage\n7)autre\n8)pas de congé \n(donner entre 1-8) :"))

    while conger != 8:
        if conger == 8:
            break
        elif conger == 1:
            print("vacances")
            #return 1
            return True
        elif conger == 2:
            print("RTT")
            #return 2
            return True
        elif conger == 3:
            print("congés maladie")
            #return 3
            return True
        elif conger == 4:
            print("jour fériés")
            #return 4
            return True
        elif conger == 5:
            print("congés de droit")
            #return 5
            return True
        elif conger == 6:
            print("mariage")
            #return 6
            return True
        elif conger == 7:
            print("autre")
            #return 7
            return True
        elif conger == 9:
            break
        conger = int(input("Entrer le type de congé:\n1)vacances\n2)RTT\n3)congés maladie\n4)jour fériés\n5)congés de droit\n6)mariage\n7)autre\n8) pas de congé \n(donner entre 1-8) :"))
    if conger == 8:
        print("pas de congé")
        return False
#     else:
#         if conger == 9:
#             print("a choisi des congés")

condition1 = type_de_conger()
#print(condition1)

# date où l'employer peut prendre des congés (jour/mois)
#date_jour = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]
#date_mois = [1,2,3,4,5,6,7,8,9,10,11,12]

date_dispo = [(5,2), (6,2), (7,2), (8,2), (9,2), (1,4), (2,4),(3,6), (4,6), (5,10), (6,10), (7,10), (25,12), (26,12), (27,12), (28,12), (28,12), (29,12), (30,12), (31,12)]

jours_pris = []

# Affichage des dates disponibles
print("Dates disponibles pour des congés :")
for date in date_dispo:
    print(f"{date[0]}/{date[1]}")

# nombre de congés que peut prendre l'employé
nbr_conger_employer = 14
"""
def nbr_de_conger(nbr_conger_employer, date_dispo):
    global jours_pris
    nbr_jours = int(input("Combien de jours de congé souhaitez-vous ? "))

#     while True:
#         if nbr_jours > nbr_conger_employer:
#             print("Au-delà de votre quota de congés, choisissez encore.")
#             nbr_jours = int(input("Combien de jours de congé souhaitez-vous ? "))
#         else:
#             jour = int(input("entrer un jour : "))
#             mois = int(input("entrer un mois : "))
#             jour_choisi = (jour,mois)
#             while True:
#                 for i in range(len(date_dispo)):
#                     jour_possible = date_dispo[i]
#                     if jour_choisi != jour_possible:
#                         jour = int(input("entrer un jour : "))
#                         mois = int(input("entrer un mois : "))
#                     else:
#                         nbr_conger_employer -= nbr_jours
#                         autre_choix = input("voulez-vous d'autre jours de congés ? (oui-non)")
#                         if nbr_conger_employer == 0:
#                             print("Vous ne pouvez plus prendre de congés.")
#                         else:
#                             print(f"Il vous restera {nbr_conger_employer} jours de congés.")
#                             if autre_choix.lower() == "oui":
#                                 jour = int(input("entrer un jour : "))
#                                 mois = int(input("entrer un mois : "))
#                             else:
#                                 return True, nbr_conger_employer
#                         break

            nbr_conger_employer -= nbr_jours
            if nbr_conger_employer == 0:
                print("Vous ne pouvez plus prendre de congés.")
            else:
                print(f"Il vous restera {nbr_conger_employer} jours de congés.")
            return True, nbr_conger_employer
"""


def nbr_de_conger(nbr_conger_employer, date_dispo):
    global jours_pris
    while nbr_conger_employer > 0:
        nbr_jours = int(input("Combien de jours de congé souhaitez-vous ? "))

        if nbr_jours > nbr_conger_employer:
            print("Au-delà de votre quota de congés, choisissez encore.")
            continue

        for _ in range(nbr_jours):
            jour = int(input("Entrez un jour : "))
            mois = int(input("Entrez un mois : "))
            jour_choisi = (jour, mois)

            if jour_choisi in date_dispo and jour_choisi not in jours_pris:
                jours_pris.append(jour_choisi)
                print(f"Jour {jour_choisi[0]}/{jour_choisi[1]} ajouté à vos congés.")
            else:
                print("Date non disponible ou déjà prise. Choisissez une autre date.")
                continue

        nbr_conger_employer -= nbr_jours
        print(f"Il vous reste {nbr_conger_employer} jours de congés.")

        autre_choix = input("Voulez-vous d'autres jours de congés ? (oui/non) ").lower()
        if autre_choix == "non":
            break

    if nbr_conger_employer == 0:
        print("Vous ne pouvez plus prendre de congés.")

    print(f"Congés pris : {jours_pris}")

    # Retourne True et le nombre de jours restants
    return True, nbr_conger_employer



condition2, nbr_conger_employer = nbr_de_conger(nbr_conger_employer, date_dispo)
#print(condition2)

# si l'employeur valide ou pas
condition3 = ""

# validation_employeur = input("l'employer peut-il prendre son congé ? (oui-non) : ")
# if validation_employeur.lower() == "oui":
#     condition3 = True
# else:
#     if validation_employeur.lower() == "non":
#         condition3 = False

validation_employeur = randint(1, 5)
if validation_employeur > 3:
    condition3 = True
else:
    condition3 = False
#print(condition3)

# vérifie que toutes les conditions sont remplies
if condition1 == True and condition2 == True and condition3 == True:
    print("Votre demande de congé est acceptée.")
else:
    if condition1 == False:
        print("ne prend aucun congé")
    elif condition2 == False:
        print("ne possède plus de congé")
    elif condition3 == False:
        print("l'employeur ne vous permet pas de prendre des congés")
    print("Votre demande de congé est rejetée.")






    # while True:
    #     nbr_jours = int(input("Combien de jours de congé souhaitez-vous ? "))
    #     if nbr_jours > nbr_conger_employer:
    #         print("Vous dépassez votre quota de congés. Essayez encore.")
    #     else:
    #         print("le nombre de jour demandé rentre dans votre quota")
    #         break