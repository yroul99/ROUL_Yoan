from item import Item

# Messages d'erreur pour les commandes incorrectes
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

class Actions:
    """
    Cette classe regroupe toutes les actions que le joueur peut exécuter via les commandes.
    Chaque méthode correspond à une commande spécifique.
    """

    @staticmethod
    def help(game, list_of_words, number_of_parameters):
        """
        Affiche la liste des commandes disponibles.
        """
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False

        print("\nVoici les commandes disponibles :")
        for command in game.commands.values():
            print("\t- " + str(command))
        print()
        return True

    @staticmethod
    def quit(game, list_of_words, number_of_parameters):
        """
        Permet de quitter le jeu.
        """
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False

        player = game.player
        print(f"\nMerci {player.name} d'avoir joué. Au revoir.\n")
        game.finished = True
        return True

    @staticmethod
    def go(game, list_of_words, number_of_parameters):
        """
        Permet au joueur de se déplacer dans une direction donnée.
        """
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG1.format(command_word=list_of_words[0]))
            return False

        direction = list_of_words[1]
        valid_directions = {
            "N": ["N", "n", "nord", "Nord", "NORD"],
            "S": ["S", "s", "sud", "Sud", "SUD"],
            "E": ["E", "e", "est", "Est", "EST"],
            "O": ["O", "o", "ouest", "Ouest", "OUEST"],
            "U": ["U", "u", "up", "Up", "UP"],
            "D": ["D", "d", "down", "Down", "DOWN"]
        }
        for key, aliases in valid_directions.items():
            if direction in aliases:
                direction = key
                break

        if direction not in game.all_directions:
            print(f"Direction {direction} non reconnue")
            return False

        game.player.move(direction)
        return True

    @staticmethod
    def charge_beamer(game, list_of_words, number_of_parameters):
        """
        Charge le beamer avec la pièce actuelle.
        """
        player = game.player
        if "beamer" not in player.inventory:
            print("\nVous devez posséder le beamer pour le charger.\n")
            return False

        player.beamer_location = player.current_room
        print("\nLe beamer a été chargé avec la pièce actuelle : " + player.current_room.name + ".\n")
        return True

    @staticmethod
    def use_beamer(game, list_of_words, number_of_parameters):
        """
        Utilise le beamer pour se téléporter à la pièce mémorisée.
        """
        player = game.player
        if "beamer" not in player.inventory:
            print("\nVous devez posséder le beamer pour l'utiliser.\n")
            return False

        if not player.beamer_location:
            print("\nLe beamer n'a pas encore été chargé.\n")
            return False

        player.current_room = player.beamer_location
        print("\nVous avez été téléporté à : " + player.current_room.name + ".\n")
        print(player.current_room.get_long_description())
        return True

    @staticmethod
    def back(game, list_of_words, number_of_parameters):
        """
        Permet au joueur de revenir à la dernière salle visitée.
        """
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False

        # Vérifier si l'historique contient suffisamment de salles pour un retour
        if len(game.player.history) < 1:
            print("\nAucun déplacement précédent. Vous êtes déjà au point de départ.\n")
            return False

        # Revenir à la dernière salle dans l'historique
        last_room = game.player.history.pop()  # Retirer la salle actuelle de l'historique
        game.player.current_room = last_room   # Mettre à jour la salle actuelle

        # Afficher la description de la pièce et l'historique mis à jour
        print(last_room.get_long_description())
        print(game.player.get_history())
        return True

    @staticmethod
    def look(game, list_of_words, number_of_parameters):
        """
        Affiche les objets et les personnages présents dans la pièce actuelle.
        """
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False

        game.player.current_room.get_inventory()
        return True

    @staticmethod
    def take(game, list_of_words, number_of_parameters):
        """
        Permet au joueur de prendre un objet présent dans la pièce actuelle.
        """
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG1.format(command_word=list_of_words[0]))
            return False

        item_name = list_of_words[1]

        for item in game.player.current_room.inventory.copy():
            if item.name.lower() == item_name.lower():
                game.player.current_room.inventory.remove(item)
                game.player.inventory[item.name] = item
                print(f"Tu as pris {item.name}.")
                return True

        print(f"L'objet {item_name} n'est pas dans cette pièce.")
        return False

    @staticmethod
    def drop(game, list_of_words, number_of_parameters):
        """
        Permet au joueur de déposer un objet de son inventaire dans la pièce actuelle.
        """
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG1.format(command_word=list_of_words[0]))
            return False

        item_name = list_of_words[1]

        if item_name.lower() in [item.lower() for item in game.player.inventory.keys()]:
            dropped_item = game.player.inventory.pop(item_name)
            game.player.current_room.inventory.add(dropped_item)
            print(f"Tu as déposé {item_name} dans la pièce.")
            return True

        print(f"L'objet {item_name} n'est pas dans ton inventaire.")
        return False

    @staticmethod
    def check(game, list_of_words, number_of_parameters):
        """
        Affiche les objets présents dans l'inventaire du joueur.
        """
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False

        game.player.get_inventory()
        return True

    @staticmethod
    def talk(game, list_of_words, number_of_parameters):
        """
        Permet au joueur de parler aux personnages présents dans la pièce actuelle.
        """
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG1.format(command_word=list_of_words[0]))
            return False

        if game.player.current_room.characters:
            for character in game.player.current_room.characters.values():
                print(character.get_msg())
        else:
            print("Il n'y a personne à qui parler.")
        return True

    @staticmethod
    def history(game, list_of_words, number_of_parameters):
        """
        Affiche l'historique des salles visitées par le joueur.
        """
        if len(list_of_words) != number_of_parameters + 1:
            print(MSG0.format(command_word=list_of_words[0]))
            return False

        game.player.get_history()
        return True

    @staticmethod
    def write(game, list_of_words, number_of_parameters):
        """
        Permet d'écrire dans un objet spécifique, comme un cahier.
        """
        if len(list_of_words) < number_of_parameters + 1:
            print(f"\nLa commande '{list_of_words[0]}' nécessite {number_of_parameters} paramètres.\n")
            return False

        object_name = list_of_words[1]
        text_to_write = " ".join(list_of_words[2:])  # Concatène tous les mots après le nom de l'objet

        # Vérifiez si l'objet est dans l'inventaire du joueur
        item = game.player.inventory.get(object_name.lower())
        if item is None:
            print(f"L'objet '{object_name}' n'est pas dans votre inventaire.")
            return False

        # Vérifiez si l'objet permet l'écriture
        if hasattr(item, "write") and callable(getattr(item, "write")):
            try:
                item.write(text_to_write)
                print(f"Vous avez écrit dans {object_name} : '{text_to_write}'.")
                return True
            except ValueError as e:
                print(e)
                return False
        else:
            print(f"L'objet '{object_name}' n'est pas utilisable pour écrire.")
            return False

        
    @staticmethod
    def check_victory(game):
        """
        Vérifie si le joueur a écrit les trois mots magiques dans le cahier de notes.
        Si oui, ajoute la clé magique à l'inventaire.
        """
        victory_clues = {"clé d'argent", "rose morte", "coffre fort"}
        player_notes = ""

        # Vérifiez si le joueur possède le cahier de notes
        for item in game.player.inventory.values():
            if item.name.lower() == "cahier_de_notes":
                player_notes = item.content.lower()
                break

        # Vérifiez si tous les mots magiques sont présents dans le cahier
        if all(clue in player_notes for clue in victory_clues):
            if "clé magique" not in game.player.inventory:
                # Ajoutez la clé magique à l'inventaire
                game.player.inventory["clé magique"] = Item(
                    "clé magique", "Une clé brillante, entourée d'une aura mystique.", 0.1
                )
                print("Félicitations ! Vous avez obtenu la clé magique.")
        else:
            print("Il vous manque encore des mots magiques pour obtenir la clé.")



    @staticmethod
    def open_coffre(game, list_of_words=None, number_of_parameters=0):
        """
        Ouvre le coffre-fort si le joueur possède la clé magique.
        """
        if "clé magique" in game.player.inventory:
            print("Vous avez ouvert le coffre-fort. À l'intérieur, vous trouvez un code mystérieux : 873876.")
            # Stocker le code dans l'inventaire ou permettre son utilisation pour déverrouiller la porte électrique
            game.player.inventory["code coffre"] = Item(
                "code coffre", "Un code à six chiffres : 873876.", 0.01
            )
        else:
            print("Vous avez besoin de la clé magique pour ouvrir le coffre-fort.")


    @staticmethod
    def enter_code(game, list_of_words, number_of_parameters):
        """
        Permet d'entrer le code pour déverrouiller la porte électrique.
        """
        if game.player.current_room.name != "Hall_d_Entrée":
            print("Vous devez être dans le Hall d'Entrée pour entrer le code de la porte électrique.")
            return False

        if "code coffre" not in game.player.inventory:
            print("Vous n'avez pas encore trouvé le code. Trouvez des indices dans le manoir pour le déterminer.")
            return False

        if len(list_of_words) != 2:
            print("\nVeuillez entrer un code. Exemple : 'enter_code 873876'")
            return False

        code_entered = list_of_words[1]
        if not hasattr(game, "attempts_left"):
            game.attempts_left = 3  # Initialisation des tentatives

        if code_entered == "873876":  # Code attendu
            print("Félicitations ! Vous avez ouvert la porte électrique et vous êtes libéré du manoir.")
            game.finished = True
            return True
        else:
            game.attempts_left -= 1
            print(f"Code incorrect. Tentatives restantes : {game.attempts_left}")

            if game.attempts_left <= 0:
                print("Vous avez épuisé vos tentatives. Vous êtes enfermé à jamais dans le manoir.")
                game.finished = True
                return True  # Arrête tout affichage supplémentaire après défaite
            return False







