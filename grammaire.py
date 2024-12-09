import os



class Grammaire:
    def __init__(self):
        self.regles = {}
        self.axiome = None

    def ajouter_regle(self, non_terminal, m_droit):
        if non_terminal not in self.regles:
            self.regles[non_terminal] = [] 
        self.regles[non_terminal].append(m_droit)

    def afficher(self):
        print("Grammaire:")
        for non_terminal, m_droit in self.regles.items():
            print(f"{non_terminal} : {' | '.join(m_droit)}")
            
    


def lire(fichier):
    if not fichier.endswith(".general"):
        raise ValueError("Le fichier ne contient pas  l'extension .general")
    
    if not os.path.exists(fichier):
        raise FileNotFoundError(f"Le fichier '{fichier}' n'existe pas.")
    
    grammaire = Grammaire()
    
    # Lecture du fichier
    with open(fichier, "r") as f:
        for ligne in f:
            ligne = ligne.strip()  # Supprimer les espaces 
            if not ligne or ":" not in ligne:
                continue 
            
            gauche, droite = ligne.split(":", 1)
            gauche = gauche.strip()
            membres_droits = [membre.strip() for membre in droite.split("|")]
            
            # Définir l'axiome si ce n'est pas encore fait
            if grammaire.axiome is None:
                grammaire.axiome = gauche
            
            # Ajouter les membres droits à la grammaire
            for membre in membres_droits:
                grammaire.ajouter_regle(gauche, membre)
    
    return grammaire


# Exemple d'utilisation
grammaire = Grammaire()
grammaire.ajouter_regle("S", "aA")
grammaire.ajouter_regle("S", "b")
grammaire.ajouter_regle("A", "cB")
grammaire.ajouter_regle("A", "d")
grammaire.axiome = "S"  # Définir l'axiome
grammaire.afficher()

# Test de la fonction lire
grammaire = lire("exemple.general")
grammaire.afficher()

