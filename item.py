class Item:
    """
    Représente un objet manipulable dans le jeu.
    """

    def __init__(self, name, description, weight):
        """
        Initialise un objet avec un nom, une description et un poids.
        """
        self.name = name
        self.description = description
        self.weight = weight
        self.content = ""  # Utilisé pour stocker du texte écrit, si applicable

    def write(self, text):
        """
        Permet d'écrire du texte dans l'objet, si applicable.
        """
        if self.name.lower() == "cahier_de_notes":
            self.content += text + "\n"  # Ajoute le texte avec une nouvelle ligne
        else:
            raise ValueError(f"Impossible d'écrire dans {self.name}. Cet objet n'est pas fait pour cela.")

    def __str__(self):
        """
        Retourne une représentation textuelle de l'objet.
        """
        if self.name.lower() == "cahier_de_notes":
            # Inclut le contenu du cahier s'il contient du texte
            contenu = f"\nContenu :\n{self.content.strip()}" if self.content else "\nContenu : (vide)"
            return f"{self.name} : {self.description} (Poids : {self.weight} kg){contenu}"
        return f"{self.name} : {self.description} (Poids : {self.weight} kg)"
