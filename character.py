import random
from random import randint




class Character:

    def __init__(self, name, description, current_room, messages=None):
        """
        Initialise un personnage avec un nom, une description, une salle actuelle, et des messages facultatifs.
        """
        self.name = name
        self.description = description
        self.current_room = current_room
        self.messages = messages if messages else []

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

    def get_msg(self):
        if len(self.msgs) != 0:
                msg = self.msgs.pop(-1)
        else:
            print("...")
        return msg
             
        


        
        
                
            


