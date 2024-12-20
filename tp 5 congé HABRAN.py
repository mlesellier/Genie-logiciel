# Créé par karlh, le 20/12/2024 en Python 3.7

import tkinter as tk
from tkinter import messagebox, simpledialog

# Classe principale pour la gestion des congés
class GestionCongesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des Congés")
        self.root.configure(bg="#f5f5f5")

        # Données de base : solde initial et demandes en attente
        self.solde_conges = {
            "Vacances": 20,
            "RTT": 10,
            "Maladie": 15
        }
        self.demandes_attente = []  # Liste des demandes en attente pour les managers
        self.types_conges = ["Vacances", "RTT", "Maladie"]

        # Interface utilisateur
        self.create_main_menu()

    def create_main_menu(self):
        # Supprimer les widgets existants
        for widget in self.root.winfo_children():
            widget.destroy()

        # Titre principal
        tk.Label(self.root, text="Gestion des Congés", font=("Arial", 18, "bold"), bg="#f5f5f5", fg="#333").pack(pady=10)

        # Boutons pour les différents rôles
        tk.Button(self.root, text="Employé", command=self.create_employee_interface, font=("Arial", 12), bg="#4CAF50", fg="white", bd=0, padx=10, pady=5).pack(pady=10)
        tk.Button(self.root, text="Manager", command=self.create_manager_interface, font=("Arial", 12), bg="#2196F3", fg="white", bd=0, padx=10, pady=5).pack(pady=10)
        tk.Button(self.root, text="RH", command=self.create_rh_interface, font=("Arial", 12), bg="#FF9800", fg="white", bd=0, padx=10, pady=5).pack(pady=10)

    def create_employee_interface(self):
        # Supprimer les widgets existants
        for widget in self.root.winfo_children():
            widget.destroy()

        # Titre principal
        tk.Label(self.root, text="Interface Employé", font=("Arial", 18, "bold"), bg="#f5f5f5", fg="#333").pack(pady=10)

        # Affichage des soldes
        self.solde_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.solde_frame.pack(pady=10)
        self.update_solde_affichage()

        # Formulaire de demande de congé
        tk.Label(self.root, text="Type de congé:", font=("Arial", 12), bg="#f5f5f5", fg="#555").pack()
        self.type_conge = tk.StringVar()
        self.type_conge.set("Vacances")
        tk.OptionMenu(self.root, self.type_conge, *self.types_conges).pack(pady=5)

        tk.Label(self.root, text="Nombre de jours:", font=("Arial", 12), bg="#f5f5f5", fg="#555").pack()
        self.nb_jours = tk.Entry(self.root, font=("Arial", 12))
        self.nb_jours.pack(pady=5)

        tk.Button(self.root, text="Soumettre Demande", command=self.demander_conge, font=("Arial", 12), bg="#4CAF50", fg="white", bd=0, padx=10, pady=5).pack(pady=10)
        tk.Button(self.root, text="Retour", command=self.create_main_menu, font=("Arial", 12), bg="#CCCCCC", fg="#333", bd=0, padx=10, pady=5).pack(pady=10)

    def create_manager_interface(self):
        # Supprimer les widgets existants
        for widget in self.root.winfo_children():
            widget.destroy()

        # Titre principal
        tk.Label(self.root, text="Interface Manager", font=("Arial", 18, "bold"), bg="#f5f5f5", fg="#333").pack(pady=10)

        # Liste des demandes
        tk.Label(self.root, text="Demandes en attente:", font=("Arial", 12), bg="#f5f5f5", fg="#555").pack()
        self.demandes_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.demandes_frame.pack(pady=5)
        self.update_demandes_affichage()

        tk.Button(self.root, text="Retour", command=self.create_main_menu, font=("Arial", 12), bg="#CCCCCC", fg="#333", bd=0, padx=10, pady=5).pack(pady=10)

    def update_demandes_affichage(self):
        for widget in self.demandes_frame.winfo_children():
            widget.destroy()

        for i, demande in enumerate(self.demandes_attente):
            demande_label = tk.Label(self.demandes_frame, text=f"{demande['employe']} - {demande['jours']} jours ({demande['type']})", font=("Arial", 12), bg="#f5f5f5", fg="#333")
            demande_label.grid(row=i, column=0, padx=5, pady=2)
            tk.Button(self.demandes_frame, text="Valider", font=("Arial", 10), bg="#4CAF50", fg="white", command=lambda d=demande: self.valider_demande(d)).grid(row=i, column=1, padx=5)
            tk.Button(self.demandes_frame, text="Refuser", font=("Arial", 10), bg="#F44336", fg="white", command=lambda d=demande: self.refuser_demande(d)).grid(row=i, column=2, padx=5)

    def valider_demande(self, demande):
        self.demandes_attente.remove(demande)
        messagebox.showinfo("Succès", f"Demande de {demande['jours']} jours pour {demande['employe']} validée.")
        self.update_demandes_affichage()

    def refuser_demande(self, demande):
        self.demandes_attente.remove(demande)
        messagebox.showinfo("Info", f"Demande de {demande['jours']} jours pour {demande['employe']} refusée.")
        self.update_demandes_affichage()

    def create_rh_interface(self):
        # Supprimer les widgets existants
        for widget in self.root.winfo_children():
            widget.destroy()

        # Titre principal
        tk.Label(self.root, text="Interface RH", font=("Arial", 18, "bold"), bg="#f5f5f5", fg="#333").pack(pady=10)

        # Gestion des types de congés
        tk.Label(self.root, text="Types de congés disponibles:", font=("Arial", 12), bg="#f5f5f5", fg="#555").pack()
        self.types_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.types_frame.pack(pady=5)
        self.update_types_affichage()

        tk.Button(self.root, text="Ajouter Type de Congé", command=self.ajouter_type_conge, font=("Arial", 12), bg="#4CAF50", fg="white", bd=0, padx=10, pady=5).pack(pady=5)
        tk.Button(self.root, text="Retour", command=self.create_main_menu, font=("Arial", 12), bg="#CCCCCC", fg="#333", bd=0, padx=10, pady=5).pack(pady=10)

    def update_types_affichage(self):
        for widget in self.types_frame.winfo_children():
            widget.destroy()

        for conge in self.types_conges:
            tk.Label(self.types_frame, text=conge, font=("Arial", 12), bg="#f5f5f5", fg="#333").pack(pady=2)

    def ajouter_type_conge(self):
        new_type = simpledialog.askstring("Nouveau Type", "Entrez le nom du nouveau type de congé:")
        if new_type and new_type not in self.types_conges:
            self.types_conges.append(new_type)
            self.solde_conges[new_type] = 0  # Initialiser le solde à 0 pour les employés
            self.update_types_affichage()
            messagebox.showinfo("Succès", f"Type de congé '{new_type}' ajouté.")

    def update_solde_affichage(self):
        # Supprime les widgets précédents
        for widget in self.solde_frame.winfo_children():
            widget.destroy()

        # Affiche les soldes
        tk.Label(self.solde_frame, text="Soldes des Congés", font=("Arial", 14, "bold"), bg="#f5f5f5", fg="#333").pack()
        for conge, solde in self.solde_conges.items():
            tk.Label(self.solde_frame, text=f"{conge}: {solde} jours restants", font=("Arial", 12), bg="#f5f5f5", fg="#555").pack()

    def demander_conge(self):
        # Récupérer les valeurs
        type_conge = self.type_conge.get()
        try:
            nb_jours = int(self.nb_jours.get())
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un nombre valide de jours.")
            return

        # Vérifier le solde disponible
        if nb_jours <= 0:
            messagebox.showerror("Erreur", "Le nombre de jours doit être positif.")
        elif type_conge not in self.solde_conges or nb_jours > self.solde_conges[type_conge]:
            messagebox.showerror("Erreur", "Solde insuffisant pour ce type de congé.")
        else:
            # Mise à jour du solde et ajout aux demandes en attente
            self.solde_conges[type_conge] -= nb_jours
            self.demandes_attente.append({"employe": "Employé A", "type": type_conge, "jours": nb_jours})
            self.update_solde_affichage()
            messagebox.showinfo("Succès", f"Votre demande de {nb_jours} jours de {type_conge} a été soumise.")

# Lancer l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = GestionCongesApp(root)
    root.mainloop()
