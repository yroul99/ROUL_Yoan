# Description: Game class

# Import modules
from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item
from character import Character
from enigme import Enigme
import tkinter as tk

DEBUG = True  # Changez en False pour désactiver les messages de débogage




class Game:



# Constructor
    def __init__(self):
        # Initialisation des attributs
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = Player("Nom par défaut", debug=DEBUG, game=self)

        self.all_directions = set()
        self.messages = []  # Liste pour stocker les messages à afficher

        # Configuration de l'interface graphique
        self.root = tk.Tk()
        self.root.title("Manoir Cabot")
        self.root.geometry("600x400")

        # Zone de texte pour afficher les messages
        self.output_text = tk.Text(self.root, state="disabled", wrap="word", height=15, width=60)
        self.output_text.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Champ d'entrée pour les commandes
        self.input_entry = tk.Entry(self.root, width=50)
        self.input_entry.grid(row=1, column=0, padx=10, pady=5)

        # Bouton pour exécuter les commandes
        self.submit_button = tk.Button(self.root, text="Entrer", command=self.process_command)
        self.submit_button.grid(row=1, column=1, padx=10, pady=5)

        # Associer la touche Entrée à la méthode process_command
        self.root.bind("<Return>", lambda event: self.process_command())

    def display_message(self, message):
        if hasattr(self, 'output_text') and self.output_text is not None:
            self.output_text.config(state="normal")
            self.output_text.insert("end", str(message) + "\n")
            self.output_text.see("end")
            self.output_text.config(state="disabled")
        else:
            print(f"[DEBUG] Le widget `output_text` n'est pas initialisé. Message : {message}")




    def add_message(self, message):
        """Ajoute un message à la liste des messages."""
        self.messages.append(message)
    
    # Setup the game
    def setup(self):

        # Setup commands
        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O, U, D)", Actions.go, 1)
        self.commands["go"] = go
        back = Command("back", " : revenir dans la salle précédente", Actions.back, 0)
        self.commands["back"] = back
        look = Command("look", " : regarder les objets présents dans la pièce", Actions.look, 0)
        self.commands["look"] = look
        take = Command("take", " <take> : prendre un objet", Actions.take, 1)
        self.commands["take"] = take
        drop = Command("drop", " <drop> : déposer un objet", Actions.drop, 1)
        self.commands["drop"] = drop
        check = Command("check", " : regarder les objets dans mon inventaire", Actions.check, 0)
        self.commands["check"] = check
        talk = Command("talk", " <personnage> : parler aux personnages présents dans la pièce", Actions.talk, 1)
        self.commands["talk"] = talk
        history = Command("history", " : afficher l'historique des salles visitées", Actions.history, 0)
        self.commands["history"] = history
        charge_beamer = Command("charge_beamer", " : charger le beamer avec la pièce actuelle", Actions.charge_beamer, 0)
        self.commands["charge_beamer"] = charge_beamer
        use_beamer = Command("use_beamer", " : utiliser le beamer pour se téléporter", Actions.use_beamer, 0)
        self.commands["use_beamer"] = use_beamer
        write = Command("write", " <objet> <texte> : écrire dans un objet (par exemple un cahier)", Actions.write, 2)
        self.commands["write"] = write
        check_victory_cmd = Command("check_victory", " : vérifie si vous avez trouvé tous les indices nécessaires", Actions.check_victory, 0)
        self.commands["check_victory"] = check_victory_cmd
        open_coffre = Command("open_coffre", " : ouvrir le coffre-fort avec la clé magique", Actions.open_coffre, 0)
        self.commands["open_coffre"] = open_coffre
        enter_code = Command("enter_code", " <code> : entrer le code pour déverrouiller la porte", Actions.enter_code, 1)
        self.commands["enter_code"] = enter_code


        # Ajoutez ces lignes lors de la création de vos salles
        enigme_salle = Enigme("Qu'est-ce qui a des clés mais ne peut pas ouvrir de serrures?", "un piano", 3)        

        # Création des pièces
        Hall_d_Entrée = Room("Hall_d_Entrée", "dans un grand hall sombre avec un lustre suspendu. Des portraits effrayants ornent les murs. Une porte électrique massive se trouve ici, verrouillée par un code mystérieux.", game=self)
        self.rooms.append(Hall_d_Entrée)
        Bibliothèque = Room("Bibliothèque", "dans une bibliothèque poussiéreuse remplie de vieux livres. Des chandelles vacillantes éclairent la pièce.", game=self)
        self.rooms.append(Bibliothèque)
        Salle_a_Manger = Room("Salle_a_Manger", "dans une salle à manger élégante avec une longue table recouverte d'une nappe poussiéreuse. Des chaises vides entourent la table.", enigme_salle, game=self)
        self.rooms.append(Salle_a_Manger)
        Chambre_Hantée = Room("Chambre_Hantée", "dans une chambre sombre avec des meubles anciens et un lit défait. Des murmures étranges résonnent dans la pièce.", game=self)
        self.rooms.append(Chambre_Hantée)
        Cave = Room("Cave", "dans une cave humide et froide avec des tonneaux et des étagères pleines de bouteilles de vin.", game=self)
        self.rooms.append(Cave)
        Jardin_Mystique = Room("Jardin_Mystique", "dans un jardin envahi par la végétation, avec des statues délabrées et un étang sombre.", game=self)
        self.rooms.append(Jardin_Mystique)
        Salle_des_Mirroirs = Room("Salle_des_Mirroirs", "dans une salle remplie de miroirs où les reflets semblent bouger de manière indépendante.", game=self)
        self.rooms.append(Salle_des_Mirroirs)
        Grenier = Room("Grenier", "dans un grenier sombre rempli de vieux objets poussiéreux et de malles abandonnées.", game=self)
        self.rooms.append(Grenier)
        Coffre_fort = Room("Coffre_fort", "dans le coffre fort rempli d'argent jusqu'à ne plus savoir quoi en faire.", game=self)
        self.rooms.append(Coffre_fort)

        # Création des sorties des pièces
        Hall_d_Entrée.exits = {"SW": Bibliothèque, "SE": Salle_a_Manger}
        Bibliothèque.exits = {"SW": Cave, "SE": Chambre_Hantée, "NW": Grenier, "NE": Hall_d_Entrée, "E": Salle_a_Manger, "S": Salle_des_Mirroirs}
        Salle_a_Manger.exits = {"NW": Hall_d_Entrée, "S": Chambre_Hantée, "W": Bibliothèque}
        Chambre_Hantée.exits = {"SW": Jardin_Mystique, "NW": Bibliothèque, "N": Salle_a_Manger, "W": Salle_des_Mirroirs}
        Cave.exits = {"NE": Bibliothèque, "N": Grenier}
        Jardin_Mystique.exits = {"NW": Salle_des_Mirroirs, "NE": Chambre_Hantée}
        Salle_des_Mirroirs.exits = {"SE": Jardin_Mystique, "NE": Salle_a_Manger, "N": Bibliothèque, "E": Chambre_Hantée}
        Grenier.exits = {"SE": Bibliothèque, "S": Cave}

        # Création des inventaires des pièces
        Bibliothèque.inventory = {Item("Aspirateur", "Un aspirateur pouvant tout aspirer", 5)}
        Salle_a_Manger.inventory = {Item("couteau", "Un simple couteau de cuisine", 0.3)}
        Chambre_Hantée.inventory = {Item("cahier_de_notes", "Un cahier de notes vide", 0.2), Item("calculatrice", "Une calculatrice scientifique", 0.2)}
        Cave.inventory = {Item("bouteille_de_vin", "Une bouteille de vin datant de 1894", 0.5)}
        Jardin_Mystique.inventory = {Item("pelle", "Une pelle permettant de fouiller le sol", 2)}
        Salle_des_Mirroirs.inventory = {Item("poupée_russe", "Une poupée russe mystérieuse", 2)}
        Grenier.inventory = {Item("coffre", "Un coffre fermé", 5), Item("beamer", "Un appareil permettant de se téléporter dans une pièce mémorisée", 1)}

       
# Characters
        Bibliothèque.characters = {
            "Roberta": Character(
                "Roberta la Réceptioniste",
                "la réceptioniste fantomatique du manoir",
                Bibliothèque,
                ["Bienvenue, aventurier ! Vous êtes piégé dans le manoir. Trouvez un moyen de percer ses secrets pour vous échapper."]
            )
        }

        Jardin_Mystique.characters = {
            "Alfred": Character(
                "Alfred le Gardien",
                "le gardien fantomatique du jardin",
                Jardin_Mystique,
                [
                    "Le premier mot est inspiré des mystères d'un vaste pays à l'Est.",
                    "Le second mot évoque la beauté fanée d'une fleur.",
                    "Le dernier mot est gravé sur une bouteille qui porte une date ancienne."
                ]
            )
        }

        Cave.characters = {
            "Maurice": Character(
                "Maurice le Fantôme",
                "un esprit érudit entouré de souvenirs du passé",
                Cave,
                ["Vous devez écrire les trois mots magiques dans le cahier de notes pour percer les mystères du manoir."]
            )
        }

        Coffre_fort.characters = {
            "Barbe Blanche": Character(
                "Le tableau qui parle de Barbe Blanche",
                "un tableau mystérieux suspendu au mur",
                Coffre_fort,
                ["Pour ouvrir ce coffre, vous devrez connaître les trois mots magiques."]
            )
        }



        # Setup player and starting room

        
        self.player = Player("Nom par défaut", debug=DEBUG, game=self)
        self.player.current_room = Hall_d_Entrée


 # Ajoutez des objets de départ au joueur
        self.player.inventory["lettre"] = Item("lettre", "Une lettre destinée à Louis Cabot datée de 1824", 0.01)
        self.player.inventory["carte"] = Item("carte", "Une carte ancienne révélant des passages secrets dans le manoir", 0.5)
        self.player.inventory["lampe_uv"] = Item("lampe_uv", "Une lampe UV pour révéler des messages cachés", 1)


        # Setup all directions
        self.all_directions = {"N", "S", "E", "W", "NE", "NW", "SE", "SW"}

    def play(self):
        self.setup()
        self.print_welcome()
        
        while not self.finished:
            user_input = input("> ")
            self.process_command(user_input)

            if self.finished:
                return  # Arrête immédiatement

            # Déplacement des PNJ
            characters_moved = set()
            for room in self.rooms:
                for character_name, character in room.characters.items():
                    if character not in characters_moved:
                        previous_room = character.current_room
                        character.move()
                        characters_moved.add(character)
                        if previous_room != character.current_room:
                            self.display_message(f"{character.name} s'est déplacé de {previous_room.name} à {character.current_room.name}.")
                        else:
                            self.display_message(f"{character.name} ne s'est pas déplacé.")



            if self.player.current_room.name == "Hall_d_Entrée":
                messages.append("La porte électrique vous bloque toujours la sortie. Entrez 'enter_code <code>' pour tenter de la déverrouiller.")
            
            Actions.check_victory(self)

            for message in messages:
                self.display_message(message)












    def process_command(self):
        command = self.input_entry.get().strip()  # Récupère la commande entrée
        self.input_entry.delete(0, "end")  # Efface l'entrée

        if not command:
            self.display_message("Veuillez entrer une commande.")
            return

        self.display_message(f"> {command}")  # Affiche la commande entrée
        self.execute_command(command)  # Exécute la commande

        if self.finished:
            self.display_message("Le jeu est terminé ! Merci d'avoir joué.")
            self.submit_button.config(state="disabled")
            self.input_entry.config(state="disabled")

    def execute_command(self, command_string):
        list_of_words = command_string.split()
        command_word = list_of_words[0]

        if command_word not in self.commands:
            self.display_message(f"Commande '{command_word}' non reconnue. Tapez 'help' pour voir les commandes disponibles.")
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)


    def start_gui(self):
        """Démarre l'interface graphique."""
        self.setup()  # Configure le jeu
        if hasattr(self, "output_text") and self.output_text is not None:
            self.display_message("""Bienvenue, aventurier courageux !

    Vous avez pénétré dans les sombres profondeurs du **manoir Cabot**, un domaine chargé de mystères et de légendes. 
    Cet héritage ancestral, autrefois le foyer d'une famille prodigieusement riche, est aujourd'hui le théâtre de récits 
    troublants où l'or et les ombres s'entrelacent.

    Votre mission ? Résoudre les énigmes des esprits tourmentés, collecter des objets précieux, et déchiffrer les 
    secrets enfouis dans chaque pièce. Les murmures disent que quelque part, caché dans le cœur du manoir, repose un 
    coffre-fort contenant une fortune inestimable. Mais attention : chaque recoin de ce lieu renferme des pièges, et 
    les fantômes des Cabot n'accordent pas facilement leur bénédiction.

    ---

    Les règles du jeu sont simples :
    - **Explorez** chaque salle et résolvez les énigmes pour progresser.
    - **Équipez-vous intelligemment** des objets trouvés, certains d'entre eux seront la clé de votre succès.
    - **Déjouez les pièges** et affrontez les esprits qui hantent ces murs.

    Votre objectif ultime ? **Ouvrir le coffre-fort et réclamer la fortune promise !**

    ---

    Un conseil avant de commencer : Ne vous fiez pas à ce que vous voyez, car dans ce manoir, tout peut être un leurre.

    Entrez 'help' pour recevoir de l'aide sur vos premières actions.

    Votre voyage commence ici... dans le Hall d'Entrée, où tout a débuté...
                                 
        """)  # Message d'accueil
        self.root.mainloop()  # Démarre la boucle principale de Tkinter



    def print_welcome(self):
        """Affiche le message d'accueil dans l'interface graphique."""
        introduction = f"""
    Bienvenue, aventurier courageux !

    Vous avez pénétré dans les sombres profondeurs du **manoir Cabot**, un domaine chargé de mystères et de légendes. 
    Cet héritage ancestral, autrefois le foyer d'une famille prodigieusement riche, est aujourd'hui le théâtre de récits 
    troublants où l'or et les ombres s'entrelacent.

    Votre mission ? Résoudre les énigmes des esprits tourmentés, collecter des objets précieux, et déchiffrer les 
    secrets enfouis dans chaque pièce. Les murmures disent que quelque part, caché dans le cœur du manoir, repose un 
    coffre-fort contenant une fortune inestimable. Mais attention : chaque recoin de ce lieu renferme des pièges, et 
    les fantômes des Cabot n'accordent pas facilement leur bénédiction.

    ---

    Les règles du jeu sont simples :
    - **Explorez** chaque salle et résolvez les énigmes pour progresser.
    - **Équipez-vous intelligemment** des objets trouvés, certains d'entre eux seront la clé de votre succès.
    - **Déjouez les pièges** et affrontez les esprits qui hantent ces murs.

    Votre objectif ultime ? **Ouvrir le coffre-fort et réclamer la fortune promise !**

    ---

    Un conseil avant de commencer : Ne vous fiez pas à ce que vous voyez, car dans ce manoir, tout peut être un leurre.

    Entrez 'help' pour recevoir de l'aide sur vos premières actions.

    Votre voyage commence ici... dans le Hall d'Entrée, où tout a débuté...
        """
        self.display_message(introduction.strip())  # Affiche l'introduction dans l'interface graphique
        self.display_message(self.player.current_room.get_long_description())  # Affiche la description de la première pièce





class GameGUI(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.title("Manoir Cabot")
        self.geometry("600x400")

        # Zone de texte pour afficher les messages du jeu
        self.output_text = tk.Text(self, state="disabled", wrap="word", height=15, width=60)
        self.output_text.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Zone de saisie pour entrer les commandes
        self.input_entry = tk.Entry(self, width=50)
        self.input_entry.grid(row=1, column=0, padx=10, pady=5)

        # Bouton pour exécuter les commandes
        self.submit_button = tk.Button(self, text="Entrer", command=self.process_command)
        self.submit_button.grid(row=1, column=1, padx=10, pady=5)

        # Lancer la boucle du jeu
        self.bind("<Return>", lambda event: self.process_command())



 
        







def main():
    game = Game()
    game.start_gui()  # Lance l'interface graphique

if __name__ == "__main__":
    main()


