class Enigme:
    def __init__(self, question, reponse_correcte, tentatives_max):
        self.question = question
        self.reponse_correcte = reponse_correcte
        self.tentatives_max = tentatives_max
        self.tentatives_actuelles = 0

    def presenter_enigme(self):
        print("\nÉnigme :")
        print(self.question)
    
    def verifier_reponse(self, reponse):
        self.tentatives_actuelles += 1
        if reponse.lower() == self.reponse_correcte.lower():
            print("Bonne réponse !")
            return True
        else:
            print("Mauvaise réponse.")
            if self.tentatives_actuelles >= self.tentatives_max:
                print(f"Vous avez épuisé toutes vos tentatives. Énigme échouée.")
                return True
            else:
                print(f"Il vous reste {self.tentatives_max - self.tentatives_actuelles} tentatives.")
                return False