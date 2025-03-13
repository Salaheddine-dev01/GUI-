import tkinter as tk
from tkinter import ttk, messagebox

class BibliothequeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion de Bibliothèque Multimédia")
        self.root.geometry("800x600")
        
        # Cadre principal
        self.main_frame = ttk.Frame(root, padding=10)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configuration de la grille
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        # Formulaire d'ajout/modification
        self._creer_formulaire()
        
        # Affichage des médias
        self._creer_treeview()
        
        # Barre d'outils
        self._creer_barre_outils()
        
        self.media_id = 1 
    
    def _creer_formulaire(self):
        self.form_frame = ttk.LabelFrame(self.main_frame, text="Ajouter/Modifier un média")
        self.form_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Type de média
        ttk.Label(self.form_frame, text="Type:").grid(row=0, column=0, padx=5, pady=5)
        self.type_var = tk.StringVar()
        self.type_combobox = ttk.Combobox(self.form_frame, textvariable=self.type_var, 
                                          values=["Livre", "DVD", "Magazine", "Livre Numérique"], state="readonly")
        self.type_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.type_combobox.bind("<<ComboboxSelected>>", self._mettre_a_jour_champs)
        
        # Titre
        ttk.Label(self.form_frame, text="Titre:").grid(row=1, column=0, padx=5, pady=5)
        self.titre_var = tk.StringVar()
        self.titre_entry = ttk.Entry(self.form_frame, textvariable=self.titre_var)
        self.titre_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Année
        ttk.Label(self.form_frame, text="Année:").grid(row=2, column=0, padx=5, pady=5)
        self.annee_var = tk.StringVar()
        self.annee_entry = ttk.Entry(self.form_frame, textvariable=self.annee_var)
        self.annee_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Cadre pour les champs dynamiques
        self.dynamic_frame = ttk.Frame(self.form_frame)
        self.dynamic_frame.grid(row=3, column=0, columnspan=2, pady=5)
    
    def _mettre_a_jour_champs(self, event=None):
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()
        
        type_selectionne = self.type_var.get()
        
        if type_selectionne == "Livre" or type_selectionne == "Livre Numérique":
            ttk.Label(self.dynamic_frame, text="Auteur:").grid(row=0, column=0, padx=5, pady=5)
            self.auteur_var = tk.StringVar()
            ttk.Entry(self.dynamic_frame, textvariable=self.auteur_var).grid(row=0, column=1, padx=5, pady=5)
            
            ttk.Label(self.dynamic_frame, text="ISBN:").grid(row=1, column=0, padx=5, pady=5)
            self.isbn_var = tk.StringVar()
            ttk.Entry(self.dynamic_frame, textvariable=self.isbn_var).grid(row=1, column=1, padx=5, pady=5)
            
            if type_selectionne == "Livre Numérique":
                ttk.Label(self.dynamic_frame, text="Taille fichier (Mo):").grid(row=2, column=0, padx=5, pady=5)
                self.taille_var = tk.StringVar()
                ttk.Entry(self.dynamic_frame, textvariable=self.taille_var).grid(row=2, column=1, padx=5, pady=5)
                
                ttk.Label(self.dynamic_frame, text="Format fichier:").grid(row=3, column=0, padx=5, pady=5)
                self.format_var = tk.StringVar()
                ttk.Combobox(self.dynamic_frame, textvariable=self.format_var, 
                              values=["PDF", "EPUB", "MOBI"], state="readonly").grid(row=3, column=1, padx=5, pady=5)
        
        elif type_selectionne == "Magazine":
            ttk.Label(self.dynamic_frame, text="Éditeur:").grid(row=0, column=0, padx=5, pady=5)
            self.editeur_var = tk.StringVar()
            ttk.Entry(self.dynamic_frame, textvariable=self.editeur_var).grid(row=0, column=1, padx=5, pady=5)
            
            ttk.Label(self.dynamic_frame, text="Périodicité:").grid(row=1, column=0, padx=5, pady=5)
            self.periodicite_var = tk.StringVar()
            ttk.Combobox(self.dynamic_frame, textvariable=self.periodicite_var, 
                         values=["Hebdomadaire", "Mensuel", "Trimestriel"], state="readonly").grid(row=1, column=1, padx=5, pady=5)
        
        elif type_selectionne == "DVD":
            ttk.Label(self.dynamic_frame, text="Réalisateur:").grid(row=0, column=0, padx=5, pady=5)
            self.realisateur_var = tk.StringVar()
            ttk.Entry(self.dynamic_frame, textvariable=self.realisateur_var).grid(row=0, column=1, padx=5, pady=5)
            
            ttk.Label(self.dynamic_frame, text="Durée (minutes):").grid(row=1, column=0, padx=5, pady=5)
            self.duree_var = tk.StringVar()
            ttk.Entry(self.dynamic_frame, textvariable=self.duree_var).grid(row=1, column=1, padx=5, pady=5)
    
    def _creer_treeview(self):
        self.tree = ttk.Treeview(self.main_frame, columns=("ID", "Type", "Titre", "Année"), show="headings")
        self.tree.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Titre", text="Titre")
        self.tree.heading("Année", text="Année")
        
        self.tree.column("ID", width=50, anchor="e")
        self.tree.column("Type", width=100, anchor="center")
        self.tree.column("Titre", width=200, anchor="w")
        self.tree.column("Année", width=80, anchor="center")
        
        # Ajouter une barre de défilement
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)
    
    def _creer_barre_outils(self):
        self.btn_frame = ttk.Frame(self.main_frame)
        self.btn_frame.grid(row=2, column=0, pady=5)
        
        ttk.Button(self.btn_frame, text="Ajouter", command=self._ajouter_media).grid(row=0, column=0, padx=5)
        ttk.Button(self.btn_frame, text="Modifier", command=self._modifier_media).grid(row=0, column=1, padx=5)
        ttk.Button(self.btn_frame, text="Supprimer", command=self._supprimer_media).grid(row=0, column=2, padx=5)
        ttk.Button(self.btn_frame, text="Détails", command=self._afficher_details).grid(row=0, column=3, padx=5)
        ttk.Button(self.btn_frame, text="Exporter", command=self._exporter_json).grid(row=0, column=4, padx=5)
    
    def _valider_donnees(self):
        if not self.titre_var.get().strip():
            messagebox.showerror("Erreur", "Le titre est obligatoire.")
            return False
        try:
            annee = int(self.annee_var.get())
            if not (1900 <= annee <= 2100):
                raise ValueError("Année invalide")
        except ValueError:
            messagebox.showerror("Erreur", "L'année doit être un nombre entre 1900 et 2100.")
            return False
        return True
    
    def _ajouter_media(self):
        if not self._valider_donnees():
            return
        
        type_media = self.type_var.get().strip()
        titre = self.titre_var.get().strip()
        annee = self.annee_var.get().strip()
        
        self.tree.insert("", "end", values=(self.media_id, type_media, titre, annee))
        self.media_id += 1
        
        # Réinitialiser le formulaire
        self.type_var.set("")
        self.titre_var.set("")
        self.annee_var.set("")
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()
    
    def _modifier_media(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Erreur", "Aucun média sélectionné.")
            return
        # Implémenter la logique de modification ici
    
    def _supprimer_media(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Erreur", "Aucun média sélectionné.")
            return
        self.tree.delete(selected_item)
    
    def _afficher_details(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Erreur", "Aucun média sélectionné.")
            return
        # Implémenter la logique d'affichage des détails ici
    
    def _exporter_json(self):
        # Implémenter la logique d'exportation en JSON ici
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = BibliothequeGUI(root)
    root.mainloop()