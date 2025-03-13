import csv
import json
from collections import namedtuple
from datetime import datetime

# Partie 1 : Modélisation des médias

class Media:
    compteur_media = 0

    def __init__(self, id, titre, annee):
        self.id = id
        self.titre = titre
        self.annee = annee
        Media.compteur_media += 1

    def afficher_details(self):
        return f"{self.titre} ({self.annee})"

    @staticmethod
    def nombre_de_medias():
        return Media.compteur_media

class Livre(Media):
    def __init__(self, id, titre, annee, auteur, isbn):
        super().__init__(id, titre, annee)
        self.auteur = auteur
        self.isbn = isbn

    def afficher_details(self):
        return f"Livre: {self.titre}, {self.annee}, {self.auteur}, ISBN: {self.isbn}"

class Magazine(Media):
    def __init__(self, id, titre, annee, editeur, periodicite):
        super().__init__(id, titre, annee)
        self.editeur = editeur
        self.periodicite = periodicite

    def afficher_details(self):
        return f"Magazine: {self.titre}, {self.annee}, {self.editeur}, {self.periodicite}"

class DVD(Media):
    def __init__(self, id, titre, annee, realisateur, duree):
        super().__init__(id, titre, annee)
        self.realisateur = realisateur
        self.duree = duree

    def afficher_details(self):
        return f"DVD: {self.titre}, {self.annee}, {self.realisateur}, Durée: {self.duree} min"

# Inheritance Multiple

class Telechargeable:
    def __init__(self, taille_fichier, format_fichier):
        self.taille_fichier = taille_fichier
        self.format_fichier = format_fichier

class LivreNumerique(Livre, Telechargeable):
    def __init__(self, id, titre, annee, auteur, isbn, taille_fichier, format_fichier):
        Livre.__init__(self, id, titre, annee, auteur, isbn)
        Telechargeable.__init__(self, taille_fichier, format_fichier)

    def afficher_details(self):
        return f"Livre Numérique: {self.titre}, {self.annee}, {self.auteur}, {self.isbn}, Taille: {self.taille_fichier}MB, Format: {self.format_fichier}"

# Partie 2 : Surcharge d'opérateurs

class CollectionMedia:
    def __init__(self):
        self.medias = []

    def __add__(self, other):
        new_collection = CollectionMedia()
        new_collection.medias = self.medias + other.medias
        return new_collection

    def __sub__(self, id):
        new_collection = CollectionMedia()
        new_collection.medias = [media for media in self.medias if media.id != id]
        return new_collection

    def __repr__(self):
        return "\n".join([media.afficher_details() for media in self.medias])

# Partie 3 : Gestion de fichiers et collections Python

Operation = namedtuple('Operation', ['media_id', 'utilisateur', 'date_operation'])

def charger_medias(fichier_csv):
    medias = []
    with open(fichier_csv, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['type'] == 'Livre':
                medias.append(Livre(int(row['id']), row['titre'], int(row['annee']), row['auteur'], row['isbn']))
            elif row['type'] == 'Magazine':
                medias.append(Magazine(int(row['id']), row['titre'], int(row['annee']), row['editeur'], row['periodicite']))
            elif row['type'] == 'DVD':
                medias.append(DVD(int(row['id']), row['titre'], int(row['annee']), row['realisateur'], int(row['duree'])))
            elif row['type'] == 'LivreNumerique':
                medias.append(LivreNumerique(int(row['id']), row['titre'], int(row['annee']), row['auteur'], row['isbn'], float(row['taille_fichier']), row['format_fichier']))
    return medias

def exporter_medias(medias, fichier_json):
    with open(fichier_json, 'w', encoding='utf-8') as file:
        json.dump([media.__dict__ for media in medias], file, ensure_ascii=False, indent=4)

# Exemple d'utilisation
if __name__ == "__main__":
    # Création de médias
    livre1 = Livre(1, "Python pour les Nuls", 2020, "John Doe", "123-456-789")
    magazine1 = Magazine(2, "Science Today", 2021, "Science Corp", "Mensuel")
    dvd1 = DVD(3, "Inception", 2010, "Christopher Nolan", 148)
    livre_num1 = LivreNumerique(4, "Apprendre Python", 2019, "Jane Doe", "987-654-321", 2.5, "PDF")

    # Collection de médias
    collection1 = CollectionMedia()
    collection1.medias = [livre1, magazine1]
    collection2 = CollectionMedia()
    collection2.medias = [dvd1, livre_num1]

    # Fusion de collections
    collection_fusionnee = collection1 + collection2
    print("Collection fusionnée:")
    print(collection_fusionnee)

    # Soustraction d'un média
    collection_reduite = collection_fusionnee - 3
    print("\nCollection après suppression du DVD:")
    print(collection_reduite)

    # Chargement et exportation de médias
    medias = charger_medias('medias.csv')
    exporter_medias(medias, 'medias.json')
