class Grammaire:
    def __init__(self):
        self.regles = {}
        self.axiome = None

    def ajouter_regle(self, non_terminal, production):
        if non_terminal not in self.regles:
            self.regles[non_terminal] = [] 
        self.regles[non_terminal].append(production)

    def afficher(self):
        print("Grammaire:")
        for non_terminal, productions in self.regles.items():
            print(f"{non_terminal} : {' | '.join(productions)}")
            
    



# Exemple d'utilisation
grammaire = Grammaire()
grammaire.ajouter_regle("S", "aA")
grammaire.ajouter_regle("S", "b")
grammaire.ajouter_regle("A", "cB")
grammaire.ajouter_regle("A", "d")
grammaire.axiome = "S"  # Définir l'axiome


grammaire.afficher()

