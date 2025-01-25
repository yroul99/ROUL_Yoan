import random
from random import randint




class Character:

    

    def __init__(self, name, description, current_room, msgs=None):
        """
        Initialise un personnage.
        :param name: Nom du personnage.
        :param description: Description du personnage.
        :param current_room: Pièce où se trouve le personnage.
        :param msgs: Liste de messages que le personnage peut transmettre.
        """
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = msgs if msgs else []

    def get_msg(self):
        """
        Retourne un message aléatoire du personnage ou un message par défaut s'il n'a rien à dire.
        """
        if self.msgs:
            return "\n".join(self.msgs)
        return f"{self.name} n'a rien à dire pour le moment."



    def move(self):
        if random.choice([True, False]):  # 50% de chance de se déplacer
            possible_exits = list(self.current_room.exits.values())
            next_room = random.choice(possible_exits)
            if next_room:
                self.current_room.characters.pop(self.name)
                self.current_room = next_room
                self.current_room.characters[self.name] = self
                return True
        return False

    def __str__(self):
            return f"{self.name} :{self.description}"


             
        


        
        
                
            


