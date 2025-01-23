import doctest

class Player:
    """
    Représente le joueur dans le jeu.
    """

 
    def __init__(self, name, max_weight=9, debug=False):
        self.name = name
        self.current_room = None
        self.history = []
        self.inventory = {}
        self.max_weight = max_weight
        self.beamer_location = None
        self.debug = debug  # Utilisez cette valeur pour activer/désactiver les messages de débogage

    def move(self, direction):
        next_room = self.current_room.get_exit(direction)
        if next_room is None:
            print("\nDirection invalide. Veuillez essayer une autre direction.\n")
            return False

        if not self.history or self.history[-1] != self.current_room:
            self.history.append(self.current_room)

        if self.debug:  # Condition pour afficher les messages de débogage
            print(f"DEBUG: Déplacement de {self.current_room.name} vers {next_room.name}")

        self.current_room = next_room
        print(self.current_room.get_long_description())
        return True



    def get_history(self):
        """
        Affiche l'historique des salles visitées.
        """
        if self.history:
            print("\nVous avez déjà visité les pièces suivantes :")
            for room in self.history:
                print(f"    - {room.name}")
        else:
            print("\nVous n'avez encore visité aucune pièce.")

    def get_inventory(self):
        """
        Retourne une description textuelle de l'inventaire du joueur
        et l'affiche dans la console.
        """
        if self.inventory:
            result = "\nVous disposez des items suivants :\n"
            for item in self.inventory.values():
                result += f"    - {item}\n"
            print(result.strip())  # Affiche dans la console
            return result.strip()  # Retourne le texte pour une utilisation ultérieure
        else:
            print("\nVotre inventaire est vide.")
            return "Votre inventaire est vide."



    def total_inventory_weight(self):
        """
        Calcule le poids total des objets dans l'inventaire.
        """
        return sum(item.weight for item in self.inventory.values())

    def can_carry(self, item):
        """
        Vérifie si le joueur peut transporter un objet supplémentaire en fonction de son poids.
        """
        return self.total_inventory_weight() + item.weight <= self.max_weight
    
    def charge_beamer(self):
        """
        Charge le beamer avec la pièce actuelle.
        """
        self.beamer_location = self.current_room
        print(f"Beamer chargé avec la pièce : {self.current_room.name}")

    def use_beamer(self):
        """
        Téléporte le joueur à la pièce mémorisée par le beamer.
        """
        if self.beamer_location:
            self.current_room = self.beamer_location
            print(f"Vous avez été téléporté à : {self.current_room.name}")
            print(self.current_room.get_long_description())  # Affiche la description de la pièce téléportée
        else:
            print("Le beamer n'est pas chargé.")
