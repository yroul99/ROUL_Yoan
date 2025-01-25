import doctest

class Player:
    """
    Représente le joueur dans le jeu.
    """
    def __init__(self, name, debug=False, game=None):
        self.name = name
        self.debug = debug
        self.current_room = None
        self.inventory = {}
        self.history = []
        self.beamer_location = None
        self.game = game  # Référence au jeu

    def move(self, direction):
        if not self.current_room or direction not in self.current_room.exits:
            self.game.display_message(f"Impossible d'aller dans cette direction : {direction}")
            return False

        # Sauvegarde de la salle actuelle dans l'historique
        self.history.append(self.current_room)
        new_room = self.current_room.exits[direction]
        self.current_room = new_room

        if self.debug:
            self.game.display_message(f"DEBUG: Déplacement de {self.history[-1].name if self.history else 'aucune'} vers {new_room.name}")
        
        # Affiche la description de la nouvelle pièce
        self.game.display_message(new_room.get_long_description())

        # Affiche les personnages présents dans la pièce
        self.game.display_message(new_room.get_characters())
        return True



           


    def get_inventory(self):
        if not self.inventory:
            self.game.display_message("Votre inventaire est vide.")
            return
        inventory_list = "\n".join([f"- {item.name}: {item.description}" for item in self.inventory.values()])
        self.game.display_message(f"Inventaire :\n{inventory_list}")


    def get_history(self):
        if not self.history:
            self.game.display_message("Vous n'avez encore visité aucune pièce.")
            return
        history_list = " ➔ ".join([room.name for room in self.history])
        self.game.display_message(f"Historique des pièces visitées :\n{history_list}")





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
        self.game.display_message(f"Beamer chargé avec la pièce : {self.current_room.name}")


    def use_beamer(self):
        """
        Téléporte le joueur à la pièce mémorisée par le beamer.
        """
        if self.beamer_location:
            self.current_room = self.beamer_location
            self.game.display_message(f"Vous avez été téléporté à : {self.current_room.name}")
            self.game.display_message(self.current_room.get_long_description())  # Affiche la description de la pièce téléportée
        else:
            self.game.display_message("Le beamer n'est pas chargé.")

