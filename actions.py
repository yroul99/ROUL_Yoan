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
        message = "Voici les commandes disponibles :\n"
        for command in game.commands.values():
            message += f"- {str(command)}\n"
        game.display_message(message)

    @staticmethod
    def quit(game, list_of_words, number_of_parameters):
        player = game.player
        game.display_message(f"Merci {player.name} d'avoir joué. Au revoir.")
        game.finished = True

    @staticmethod
    def go(game, list_of_words, number_of_parameters):
        direction = list_of_words[1]
        valid_directions = {"N", "S", "E", "W", "NE", "NW", "SE", "SW"}
        if direction not in valid_directions:
            game.display_message(f"Direction non reconnue : {direction}")
            return False

        game.player.move(direction)
        return True

    @staticmethod
    def charge_beamer(game, list_of_words, number_of_parameters):
        player = game.player
        if "beamer" not in player.inventory:
            game.display_message("\nVous devez posséder le beamer pour le charger.\n")
            return False

        player.beamer_location = player.current_room
        game.display_message("\nLe beamer a été chargé avec la pièce actuelle : " + player.current_room.name + ".\n")
        return True

    @staticmethod
    def use_beamer(game, list_of_words, number_of_parameters):
        player = game.player
        if "beamer" not in player.inventory:
            game.display_message("\nVous devez posséder le beamer pour l'utiliser.\n")
            return False

        if not player.beamer_location:
            game.display_message("\nLe beamer n'a pas encore été chargé.\n")
            return False

        player.current_room = player.beamer_location
        game.display_message("\nVous avez été téléporté à : " + player.current_room.name + ".\n")
        game.display_message(player.current_room.get_long_description())
        return True

    @staticmethod
    def back(game, list_of_words, number_of_parameters):
        """
        Permet au joueur de revenir à la dernière salle visitée.
        """
        if len(list_of_words) != number_of_parameters + 1:
            game.display_message(f"\nLa commande '{list_of_words[0]}' ne prend pas de paramètre.\n")
            return False

        if not game.player.history:
            game.display_message("\nAucun déplacement précédent. Vous êtes déjà au point de départ.\n")
            return False

        last_room = game.player.history.pop()  # Retirer la dernière pièce de l'historique
        game.player.current_room = last_room  # Mettre à jour la salle actuelle
        game.display_message(last_room.get_long_description())  # Afficher la description de la salle

        # Affiche l'historique restant
        history = " ➔ ".join(room.name for room in game.player.history) if game.player.history else "Aucune"
        game.display_message(f"Historique des pièces visitées : {history}")
        return True


    @staticmethod
    def look(game, list_of_words, number_of_parameters):
        if len(list_of_words) != number_of_parameters + 1:
            game.display_message(MSG0.format(command_word=list_of_words[0]))
            return False

        room = game.player.current_room
        # Afficher l'inventaire de la pièce
        game.display_message("Objets dans cette pièce :")
        game.display_message(room.get_inventory())

        # Afficher les personnages présents
        game.display_message("Personnages dans cette pièce :")
        game.display_message(room.get_characters())
        return True

    @staticmethod
    def take(game, list_of_words, number_of_parameters):
        item_name = list_of_words[1]
        for item in game.player.current_room.inventory.copy():
            if item.name.lower() == item_name.lower():
                game.player.current_room.inventory.remove(item)
                game.player.inventory[item.name] = item
                game.display_message(f"Tu as pris {item.name}.")
                return True

        game.display_message(f"L'objet {item_name} n'est pas dans cette pièce.")
        return False

    @staticmethod
    def drop(game, list_of_words, number_of_parameters):
        item_name = list_of_words[1]
        if item_name.lower() in [item.lower() for item in game.player.inventory.keys()]:
            dropped_item = game.player.inventory.pop(item_name)
            game.player.current_room.inventory.add(dropped_item)
            game.display_message(f"Tu as déposé {item_name} dans la pièce.")
            return True

        game.display_message(f"L'objet {item_name} n'est pas dans ton inventaire.")
        return False

    def check(game, list_of_words, number_of_parameters):
        """
        Affiche les objets présents dans l'inventaire du joueur.
        """
        if len(list_of_words) != number_of_parameters + 1:
            game.display_message(MSG0.format(command_word=list_of_words[0]))
            return False

        inventory = game.player.inventory
        if not inventory:
            game.display_message("Votre inventaire est vide.")
            return True

        message = "Inventaire :"
        for item in inventory.values():
            message += f"\n- {item.name}: {item.description}"
            # Vérifiez si l'objet a un attribut "content" non vide
            if hasattr(item, "content") and item.content.strip():
                message += f"\n  Contenu : {item.content}"

        game.display_message(message)
        return True


    @staticmethod
    def talk(game, list_of_words, number_of_parameters):
        if len(list_of_words) != number_of_parameters + 1:
            game.display_message(MSG1.format(command_word=list_of_words[0]))
            return False

        character_name = list_of_words[1]
        if character_name in game.player.current_room.characters:
            character = game.player.current_room.characters[character_name]
            game.display_message(character.get_msg())
        else:
            game.display_message(f"Il n'y a personne nommé {character_name} dans cette pièce.")
        return True


    @staticmethod
    def history(game, list_of_words, number_of_parameters):
        history = game.player.get_history()
        game.display_message(history)

    @staticmethod
    def write(game, list_of_words, number_of_parameters):
        """
        Permet d'écrire dans un objet.
        """
        if len(list_of_words) < 3:
            game.display_message("Erreur : Il faut spécifier un objet et un texte à écrire.")
            return False

        item_name = list_of_words[1]
        text = " ".join(list_of_words[2:])

        if item_name in game.player.inventory:
            item = game.player.inventory[item_name]
            if hasattr(item, "content"):
                item.content = (item.content + f" {text}").strip()  # Ajoute le texte au contenu existant
                game.display_message(f"Vous avez écrit dans {item_name} : '{text}'.")
                Actions.check_victory(game)  # Vérifie immédiatement après chaque écriture
            else:
                game.display_message(f"Vous ne pouvez pas écrire dans {item_name}.")
        else:
            game.display_message(f"Vous ne possédez pas l'objet {item_name}.")
        return True

        
    @staticmethod
    def check_victory(game):
        """
        Vérifie si le joueur a écrit les trois mots magiques dans le cahier de notes.
        Si oui, ajoute la clé magique à l'inventaire.
        """
        victory_clues = {"la Russie", "rose morte", "Année 1894"}
        player_notes = ""

        # Vérifiez si le joueur possède le cahier de notes
        for item in game.player.inventory.values():
            if item.name.lower() == "cahier_de_notes":
                player_notes = item.content.lower() if hasattr(item, "content") else ""
                break

        # Vérifiez si tous les mots magiques sont présents dans le cahier
        if all(clue.lower() in player_notes for clue in victory_clues):
            if "clé magique" not in game.player.inventory:
                # Ajoutez la clé magique à l'inventaire
                game.player.inventory["clé magique"] = Item(
                    "clé magique", "Une clé brillante, entourée d'une aura mystique.", 0.1
                )
                game.display_message("Félicitations ! Vous avez obtenu la clé magique.")
            else:
                game.display_message("Vous avez déjà la clé magique.")
        else:
            # Message générique sans révéler les mots manquants
            game.display_message("Il vous manque encore des indices pour obtenir la clé magique.")





    
    @staticmethod
    def check_inventory(game, list_of_words, number_of_parameters):
        """
        Affiche l'inventaire actuel du joueur dans l'interface graphique.
        """
        inventory = game.player.get_inventory()
        game.display_message(inventory)




    @staticmethod
    def open_coffre(game, list_of_words=None, number_of_parameters=0):
        if "clé magique" in game.player.inventory:
            game.display_message("Vous avez ouvert le coffre-fort. À l'intérieur, vous trouvez un code mystérieux : 873876.")
            game.player.inventory["code coffre"] = Item("code coffre", "Un code à six chiffres : 873876.", 0.01)
        else:
            game.display_message("Vous avez besoin de la clé magique pour ouvrir le coffre-fort.")



    @staticmethod
    def enter_code(game, list_of_words, number_of_parameters):
        """
        Permet d'entrer le code pour déverrouiller la porte électrique.
        """
        if game.player.current_room.name != "Hall_d_Entrée":
            game.display_message("Vous devez être dans le Hall d'Entrée pour entrer le code de la porte électrique.")
            return False

        if "code coffre" not in game.player.inventory:
            game.display_message("Vous n'avez pas encore trouvé le code. Trouvez des indices dans le manoir pour le déterminer.")
            return False

        if len(list_of_words) != 2:
            game.display_message("\nVeuillez entrer un code. Exemple : 'enter_code 873876'")
            return False

        code_entered = list_of_words[1]
        if not hasattr(game, "attempts_left"):
            game.attempts_left = 3  # Initialisation des tentatives

        if code_entered == "873876":  # Code attendu
            game.display_message("Félicitations ! Vous avez ouvert la porte électrique et vous êtes libéré du manoir.")
            game.finished = True
            return True
        else:
            game.attempts_left -= 1
            game.display_message(f"Code incorrect. Tentatives restantes : {game.attempts_left}")

            if game.attempts_left <= 0:
                game.display_message("Vous avez épuisé vos tentatives. Vous êtes enfermé à jamais dans le manoir.")
                game.finished = True
                return True
            return False








