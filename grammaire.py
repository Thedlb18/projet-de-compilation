import os
from collections import defaultdict
import sys
sys.stdout.reconfigure(encoding='utf-8')





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
            
    def generer_nom_non_terminal(self, prefixe):
        compteur = 0
        while f"{prefixe}{compteur}" in self.regles:
            compteur += 1
        return f"{prefixe}{compteur}"

    
    
    
    def chomsky(self):
        print("Début de la transformation en forme normale de Chomsky")
        nouvelle_grammaire = Grammaire()
        nouvelle_grammaire.axiome = self.axiome

        # Étape 1 : Ajouter un nouvel axiome si nécessaire
        if any(self.axiome in regle for regles in self.regles.values() for regle in regles):
            nouvel_axiome = self.generer_nom_non_terminal("S")
            print(f"Axiome trouvé dans les règles. Création d'un nouvel axiome : {nouvel_axiome}")
            nouvelle_grammaire.ajouter_regle(nouvel_axiome, self.axiome)
            for regle in self.regles[self.axiome]:
                nouvelle_grammaire.ajouter_regle(self.axiome, regle)

        else:
            print("Pas de nouvel axiome nécessaire.")

        
        print(f"Grammaire après étape 1 : nouvelle_grammaire.regles")
            

        # Étape 2 : Remplacement des terminaux dans les règles longues
        print("Étape 2 : Suppression des terminaux dans les règles longues")
        terminal_map = {}
        nouvelles_regles = defaultdict(list)  # Utiliser un dictionnaire temporaire pour les nouvelles règles

        for non_terminal, regles in list(nouvelle_grammaire.regles.items()):  # Parcourir une copie
            for regle in regles:
                nouvelle_regle = ""
                modifiee = False  # Indique si une règle a été modifiée
                for symbole in regle:
                    if symbole.islower():  # Si le symbole est un terminal
                        if symbole not in terminal_map:  # Créer un nouveau non-terminal pour ce terminal
                            nouveau_nt = nouvelle_grammaire.generer_nom_non_terminal("T")
                            terminal_map[symbole] = nouveau_nt
                            nouvelle_grammaire.ajouter_regle(nouveau_nt, symbole)
                            print(f"Création de terminal : {nouveau_nt} -> {symbole}")
                        nouvelle_regle += terminal_map[symbole]
                        modifiee = True
                    else:
                        nouvelle_regle += symbole

                # Ajouter la règle modifiée ou non à la grammaire temporaire
                if modifiee:  # Si la règle a été modifiée, ajoutez la nouvelle version
                    if nouvelle_regle not in nouvelles_regles[non_terminal]:
                        nouvelles_regles[non_terminal].append(nouvelle_regle)
                        print(f"Nouvelle règle après suppression des terminaux : {non_terminal} -> {nouvelle_regle}")
                else:  # Sinon, conservez la règle originale
                    if regle not in nouvelles_regles[non_terminal]:
                        nouvelles_regles[non_terminal].append(regle)

        # Mettre à jour la grammaire avec les nouvelles règles
        nouvelle_grammaire.regles = nouvelles_regles
        print(f"Grammaire après étape 2 : {nouvelle_grammaire.regles}")




        # Étape 3 : Suppression des longues règles
        print("Étape 3 : Suppression des longues règles")
        nouvelles_regles = defaultdict(list)  # Utiliser un dictionnaire temporaire pour les nouvelles règles

        for non_terminal, regles in list(nouvelle_grammaire.regles.items()):  # Parcourir une copie
            for regle in regles:
                if len(regle) > 2:  # Identifier les longues règles
                    print(f"Décomposition de la règle longue : {non_terminal} -> {regle}")
                    nouvelle_regle = regle

                    while len(nouvelle_regle) > 2:
                        # Créer un nouveau non-terminal pour le reste
                        nouveau_non_terminal = nouvelle_grammaire.generer_nom_non_terminal("X")
                        prefixe = nouvelle_regle[0]  # Premier symbole
                        reste = nouvelle_regle[1:]  # Tout sauf le premier symbole

                        # Éviter les auto-références
                        if reste == nouveau_non_terminal:
                            print(f"Erreur évitée : auto-référence détectée pour {nouveau_non_terminal}")
                            break

                        # Ajouter une règle pour le reste
                        if reste not in nouvelles_regles[nouveau_non_terminal]:
                            nouvelles_regles[nouveau_non_terminal].append(reste)
                            print(f"Création : {nouveau_non_terminal} -> {reste}")

                        # Réduire la règle
                        nouvelle_regle = prefixe + nouveau_non_terminal
                        print(f"Nouvelle règle réduite : {nouvelle_regle}")

                    # Ajouter la règle réduite finale
                    if nouvelle_regle not in nouvelles_regles[non_terminal]:
                        nouvelles_regles[non_terminal].append(nouvelle_regle)
                else:
                    # Ajouter directement les règles courtes
                    if regle not in nouvelles_regles[non_terminal]:
                        nouvelles_regles[non_terminal].append(regle)

        # Mettre à jour la grammaire avec les nouvelles règles
        nouvelle_grammaire.regles = nouvelles_regles
        print(f"Règles après étape 3 : {nouvelle_grammaire.regles}")












        # Étape 4 : Suppression des ε-règles
        print("Étape 4 : Suppression des ε-règles")

        # Identifier les non-terminaux pouvant produire ε
        epsilon_non_terminaux = {nt for nt, regles in nouvelle_grammaire.regles.items() if "E" in regles}

        while epsilon_non_terminaux:
            nt = epsilon_non_terminaux.pop()  # Prendre un non-terminal qui produit ε
            print(f"Suppression des ε-productions pour : {nt}")

            for nt2, regles in list(nouvelle_grammaire.regles.items()):
                nouvelles_regles = []
                for regle in regles:
                    if nt in regle:  # Si le non-terminal est dans la règle
                        # Générer toutes les alternatives possibles
                        alternatives = [regle[:i] + regle[i+1:] for i in range(len(regle)) if regle[i] == nt]
                        for alt in alternatives:
                            if alt not in nouvelles_regles:  # Éviter les doublons
                                nouvelles_regles.append(alt)
                # Ajouter les nouvelles règles générées
                nouvelle_grammaire.regles[nt2].extend(filter(None, nouvelles_regles))

            # Supprimer la règle ε si elle est encore présente
            if "E" in nouvelle_grammaire.regles[nt]:
                nouvelle_grammaire.regles[nt].remove("E")
                print(f"Règle ε supprimée pour : {nt}")

        print(f"Règles après étape 4 : {nouvelle_grammaire.regles}")


        # Étape 5 : Suppression des règles unitaires
        print("Étape 5 : Suppression des règles unitaires")

        for nt, regles in list(nouvelle_grammaire.regles.items()):
            unitaires = [regle for regle in regles if regle in nouvelle_grammaire.regles]
            for unitaire in unitaires:
                nouvelle_grammaire.regles[nt].remove(unitaire)
                for regle in nouvelle_grammaire.regles[unitaire]:
                    if regle not in nouvelle_grammaire.regles[nt]:  # Éviter les doublons
                        nouvelle_grammaire.regles[nt].append(regle)

        print(f"Règles après étape 5 : {nouvelle_grammaire.regles}")


        print("Fin de la transformation")
        return nouvelle_grammaire



       
       
    
     
    


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
grammaire.ajouter_regle("S9", "aA")
grammaire.ajouter_regle("S", "b")
grammaire.ajouter_regle("A", "cB")
grammaire.ajouter_regle("A", "d")
grammaire.axiome = "S"  # Définir l'axiome
grammaire.afficher()

# Test de la fonction lire
grammaire = lire("exemple.general")
grammaire.afficher()

#Test de chomsky
grammaire = Grammaire()
grammaire.ajouter_regle("S", "aSa")
grammaire.ajouter_regle("S", "bSb")
grammaire.ajouter_regle("S", "a")
grammaire.ajouter_regle("S", "b")
grammaire.ajouter_regle("S", "E")
grammaire.axiome = "S"

resultat = grammaire.chomsky()
resultat.afficher()
