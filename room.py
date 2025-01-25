# Define the Room class.
from item import Item
from enigme import Enigme

class Room:
    """
    Représente une pièce dans le jeu, contenant des sorties, des objets, des personnages et éventuellement une énigme.
    """

class Room:
    """
    Représente une pièce dans le jeu.
    """

    def __init__(self, name, description, enigme=None, game=None):
        """
        Initialise une pièce avec un nom, une description et éventuellement une énigme.
        :param name: Nom de la pièce
        :param description: Description de la pièce
        :param enigme: Une instance d'énigme, par défaut None
        :param game: Référence au jeu, par défaut None
        """
        self.name = name
        self.description = description
        self.enigme = enigme
        self.inventory = set()  # Inventaire de la pièce
        self.exits = {}  # Dictionnaire des sorties
        self.characters = {}  # Dictionnaire des personnages présents
        self.game = game  # Référence au jeu

    def presenter_enigme(self):
        if self.enigme:
            self.game.display_message(f"\n✨ Énigme : {self.enigme.question}")
            tentative = self.game.input("Votre réponse : ")  # Utiliser l'entrée graphique

            if tentative.lower() == self.enigme.reponse_correcte.lower():
                self.game.display_message("Bravo ! Vous avez résolu l'énigme.")
                return True

            self.enigme_tentatives += 1
            if self.enigme_tentatives >= self.enigme.tentatives_max:
                self.game.display_message("Vous avez épuisé toutes vos tentatives. Vous avez perdu.")
                self.game.finished = True

        return False


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
        if self.inventory:
            return "\n".join([f"- {item.name}: {item.description}" for item in self.inventory])
        return "Il n'y a aucun objet dans cette pièce."

    def get_characters(self):
        """
        Retourne une description des personnages présents dans la pièce.
        """
        if not self.characters:
            return "Il n'y a aucun personnage dans cette pièce."
        return "\n".join([f"- {character.name}: {character.description}" for character in self.characters.values()])



