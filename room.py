# Define the Room class.
from item import Item
from enigme import Enigme

class Room:
    """
    Représente une pièce dans le jeu, contenant des sorties, des objets, des personnages et éventuellement une énigme.
    """

    def __init__(self, name, description, enigme=None):
        """
        Initialise une pièce avec un nom, une description, des sorties, des objets, des personnages et une énigme éventuelle.
        """
        self.name = name
        self.description = description
        self.exits = {}  # Dictionnaire des sorties
        self.inventory = set()  # Inventaire des objets dans la pièce
        self.characters = {}  # Dictionnaire des personnages dans la pièce
        self.enigme = enigme  # Énigme associée à la pièce
        self.enigme_tentatives = 0  # Compteur de tentatives pour résoudre l'énigme

    def get_exit(self, direction):
        """
        Retourne la pièce dans la direction donnée, si elle existe.
        """
        return self.exits.get(direction, None)

    def get_exit_string(self):
        """
        Retourne une chaîne décrivant les sorties disponibles dans la pièce.
        """
        if not self.exits:
            return "Il n'y a pas de sorties disponibles."
        exit_string = "Sorties: " + ", ".join(self.exits.keys())
        return exit_string

    def get_long_description(self):
        """
        Retourne une description complète de la pièce, y compris ses sorties.
        """
        return f"\nVous êtes {self.description}\n\n{self.get_exit_string()}\n"

    def get_inventory(self):
        """
        Affiche les objets et personnages présents dans la pièce.
        """
        # Afficher les objets présents
        if self.inventory:
            print("\nLa pièce contient les objets suivants :")
            for item in self.inventory:
                print(f"    - {item.name}: {item.description} ({item.weight} kg)")
        else:
            print("\nIl n'y a aucun objet dans cette pièce.")

        # Afficher les personnages présents
        if self.characters:
            print("\nLes personnages suivants sont présents :")
            for character in self.characters.values():
                print(f"    - {character.name}: {character.description}")
        else:
            print("\nIl n'y a aucun personnage dans cette pièce.")

    def presenter_enigme(self):
        """
        Présente une énigme au joueur et vérifie sa réponse.
        """
        if self.enigme:
            print("\nÉnigme :")
            print(self.enigme.question)
            tentative = input("Votre réponse : ")

            # Vérifiez si la réponse est correcte
            if tentative.lower() == self.enigme.reponse_correcte.lower():
                print("Bravo ! Vous avez résolu l'énigme.")
                return True
            else:
                print("Mauvaise réponse. Essaie encore.")
                self.enigme_tentatives += 1

                # Si les tentatives sont épuisées, affichez un message et terminez le jeu
                if self.enigme_tentatives >= self.enigme.tentatives_max:
                    print("Vous avez épuisé toutes vos tentatives. Vous avez perdu.")
                    exit()

        return False
