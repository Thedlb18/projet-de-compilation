from grammaire import Grammaire, lire


class Greibach(Grammaire):
    def __init__(self):
        super().__init__()

    def retirer_axiome_des_membres_droits(self):
        """1. Retirer l’axiome des membres droits des règles."""
        for nt, regles in self.regles.items():
            self.regles[nt] = [r for r in regles if r != self.axiome]

    def enlever_epsilon(self):
        """Supprimer les règles X → ε sauf si X est l’axiome."""
        epsilon_produisant = {nt for nt, regles in self.regles.items() if "E" in regles}
        while epsilon_produisant:
            nt = epsilon_produisant.pop()
            self.regles[nt] = [r for r in self.regles[nt] if r != "E"]
            for gauche, regles in self.regles.items():
                nouvelles_regles = []
                for regle in regles:
                    if nt in regle:
                        # Ajouter les règles sans le NT
                        nouvelles_regles += self._generer_regles_sans_non_terminal(regle, nt)
                self.regles[gauche] += nouvelles_regles

    def _generer_regles_sans_non_terminal(self, regle, nt):
        """Générer toutes les combinaisons possibles en retirant un NT."""
        resultats = [regle]
        while nt in regle:
            regle = regle.replace(nt, "", 1)
            resultats.append(regle)
        return list(set(resultats))

    def supprimer_unite(self):
        """Supprimer les règles unité X → Y."""
        for nt in list(self.regles.keys()):
            regles_unitaires = [r for r in self.regles[nt] if len(r) == 2 and r.isalnum()]
            for regle in regles_unitaires:
                self.regles[nt].remove(regle)
                self.regles[nt] += self.regles.get(regle, [])

    def supprimer_non_terminaux_en_tete(self):
        """Supprimer les non-terminaux en tête des règles."""
        for nt in list(self.regles.keys()):
            nouvelles_regles = []
            for regle in self.regles[nt]:
                if regle[0].islower():  # Si un terminal est déjà en tête
                    nouvelles_regles.append(regle)
                else:
                    premier_nt = regle[:2]
                    reste = regle[2:]
                    nouvelles_regles += [prod + reste for prod in self.regles.get(premier_nt, [])]
            self.regles[nt] = nouvelles_regles

    def supprimer_symboles_terminaux_non_en_tete(self):
        """Supprimer les symboles terminaux qui ne sont pas en tête des règles."""
        for nt, regles in self.regles.items():
            nouvelles_regles = []
            for regle in regles:
                if regle[0].islower():
                    nouvelles_regles.append(regle)
                else:
                    premier_nt = regle[:2]
                    suffixe = regle[2:]
                    nouvelles_regles += [t + suffixe for t in self.regles.get(premier_nt, [])]
            self.regles[nt] = nouvelles_regles

    def convertir_greibach(self):
        """Appliquer toutes les étapes pour convertir la grammaire en FNG."""
        self.retirer_axiome_des_membres_droits()
        self.enlever_epsilon()
        self.supprimer_unite()
        self.supprimer_non_terminaux_en_tete()
        self.supprimer_symboles_terminaux_non_en_tete()

    def generer_mots(self, longueur_max):
        """Générer tous les mots de longueur <= longueur_max."""
        resultats = set()

        def generer(chaine, longueur):
            if longueur > longueur_max:
                return
            if all(c.islower() for c in chaine):
                resultats.add(chaine)
                return
            for i, c in enumerate(chaine):
                if c.isupper():
                    for production in self.regles[c]:
                        generer(chaine[:i] + production + chaine[i + 1:], longueur + len(production) - 1)
                    break

        generer(self.axiome, 0)
        return sorted(resultats)

# Exemple d'utilisation
if __name__ == "__main__":
    # Charger la grammaire depuis un fichier
    fichier = "exemple.general"
    grammaire = lire(fichier)

    # Transformer en forme normale de Greibach
    greibach = Greibach()
    greibach.regles = grammaire.regles
    greibach.axiome = grammaire.axiome

    # Appliquer la conversion
    greibach.convertir_greibach()

    # Afficher la grammaire convertie
    greibach.afficher()

    # Générer des mots
    mots = greibach.generer_mots(5)
    print("Mots generes :", mots)
